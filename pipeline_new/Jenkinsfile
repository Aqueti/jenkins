#!/usr/bin/env groovy

pipeline {    
  agent none
   
  options {
    timeout(time: 1, unit: 'HOURS')
  }
  
  environment {
      BRANCH_NAME = 'master'
  }

   stages {
      stage('Parallel build') {           
        failFast true
        parallel {
        stage('Compiler: build api and daemon') {
          agent { label "compiler" }
          steps {
            git branch: 'v2.0', credentialsId: '', url: 'https://github.com/Aqueti/acos.git'
            
            stash includes: "release_notes.txt", name: 'release_notes'
           
            sh "mkdir -p build_acos"
            dir('build_acos') {
               sh "cmake .. -DBUILD_ACI:BOOL=OFF -DBUILD_AGT:BOOL=ON -DBUILD_API:BOOL=ON -DBUILD_APPLICATIONS:BOOL=OFF -DBUILD_DEB_PACKAGE:BOOL=ON -DBUILD_EXAMPLES:BOOL=OFF -DBUILD_OPENCV:BOOL=OFF -DBUILD_TESTS:BOOL=ON -DSET_MOD_VER:BOOL=ON -DUSE_DOXYGEN:BOOL=OFF -DUSE_SUPERBUILD:BOOL=ON -DVERSION_TAG=${env.BRANCH_NAME}"
               sh "make -j48"

              dir('INSTALL/deb') {
                stash includes: 'AquetiAPI-linux64*.deb', name: 'AquetiAPI'
                stash includes: 'AquetiDaemon-x86_64*.deb', name: 'AquetiDaemon_x86_64'             
              }                
            }

          }
          
          post {  
            always { 
              deleteDir()
            }
          }
        }
                
        stage('Tegra: build acosd') {
          agent { label "tegra_compiler" }
        
          steps {            
            git branch: 'tegra_acosd', credentialsId: '', url: 'https://github.com/Aqueti/acos.git'
              
            sh "mkdir -p build_acosd"
            dir('build_aci') {
               sh "cmake ../ -DBUILD_ACI:BOOL=ON -DBUILD_AGT:BOOL=OFF -DBUILD_API:BOOL=OFF -DBUILD_APPLICATIONS:BOOL=OFF -DBUILD_DEB_PACKAGE:BOOL=ON -DBUILD_EXAMPLES:BOOL=OFF -DBUILD_OPENCV:BOOL=OFF -DBUILD_TESTS:BOOL=OFF -DUSE_DOXYGEN:BOOL=OFF -DSET_MOD_VER:BOOL=ON -DUSE_HTTPS:BOOL=ON -DVERSION_TAG=${env.BRANCH_NAME}"
               //sh "make -j4"
               sh "make -j4 aci"

              dir('INSTALL/deb') {
                stash includes: 'aci*.deb', name: 'aci'             
              }
            }
          }
          
          post {  
            always {    
               deleteDir()
            }
          }
        }

        stage('Tegra: build daemon') {
          agent { label "tegra_compiler" }
        
          steps {
            git branch: 'tegra_daemon', credentialsId: '', url: 'https://github.com/Aqueti/acos.git'
           
            sh "mkdir -p build_daemon"
            dir('build_daemon') {
               sh "cmake ../ -DBUILD_ACI:BOOL=ON -DBUILD_AGT:BOOL=OFF -DBUILD_API:BOOL=OFF -DBUILD_APPLICATIONS:BOOL=OFF -DBUILD_DEB_PACKAGE:BOOL=ON -DBUILD_EXAMPLES:BOOL=OFF -DBUILD_OPENCV:BOOL=OFF -DBUILD_TESTS:BOOL=OFF -DUSE_DOXYGEN:BOOL=OFF -DSET_MOD_VER:BOOL=ON -DUSE_HTTPS:BOOL=ON -DVERSION_TAG=${env.BRANCH_NAME}"
               //sh "make -j4"
               sh "make -j4 daemon"

              dir('INSTALL/deb') { 
                stash includes: 'AquetiDaemon*.deb', name: 'AquetiDaemon-aarch64'             
              }
            }
          }
          
          post {  
            always {    
               deleteDir()
            }
          }
        }
        }
      }
 
      stage('Pack Homunculus') {
            agent { label "master" }
        
            steps {
                git credentialsId: '', url: 'https://github.com/Aqueti/applications.git'

                //dir('applications') {
                  sh 'tar -cvzf homunculus.tar.gz Homunculus'
                  stash includes: 'homunculus.tar.gz', name: 'homunculus'
                //}
            }
            
            post {  
                always {    
                   deleteDir()
            }
          }
        }
      
      stage('Deploy') {
         agent { label 'master' }
         
         steps {                 
            echo "Deploy"
            
            git branch: 'master', credentialsId: '', url: 'https://github.com/Aqueti/jenkins.git' 
            
            sh "mkdir -p deploy/${env.BRANCH_NAME}/${env.BUILD_NUMBER}"
            dir("deploy/${BRANCH_NAME}/${BUILD_NUMBER}") {
                //unstash 'release_notes'
                unstash 'AquetiDaemon-aarch64'
                unstash 'AquetiDaemon_x86_64'
                unstash 'AquetiAPI'
                unstash 'homunculus'
                unstash 'aci'
                
                sh "../../../pipeline_new/bash/genReleasePage.sh ${BRANCH_NAME} ${BUILD_NUMBER}"
                sh "../../../pipeline_new/bash/genMainPage.sh ${env.BRANCH_NAME} ${BUILD_NUMBER}"
            }
            
            sh "rm -rf deploy"
         }
      }
      
      stage('Build docker container') {
         agent { label 'master' }
        
         steps {
            dir('docker') {
              dir('install') {
                unstash 'AquetiAPI'
                unstash 'homunculus'
              }
         
              sh 'echo "" | sudo -S docker build -t aqueti/${BRANCH_NAME}:${BUILD_NUMBER} .'
            }
            
            sh 'echo "" | sudo docker login -u ${docker_hub_username} -p ${docker_hub_password}'
            sh 'echo "" | sudo docker push aqueti/${BRANCH_NAME}:${BUILD_NUMBER}'
         }
         post {  
            always {    
               deleteDir()
            }
          }
      }
      
      stage('Setup test env') {
         agent { label 'cam_server' }
         steps {
            echo ""
         }
         
         post {  
            always {    
               deleteDir()
            }
         }
      }
      
      stage('Run tests') {
         agent { label 'cam_server' }
         steps {
            echo ""
         }
         
        post {  
            always {    
               deleteDir()
            }
        }
      }
    }

  post { 
    always {      
     echo 'always'
    }
 
    success {       
       emailext(
          recipientProviders: [[$class: 'RequesterRecipientProvider']],
          to: "astepenko@aqueti.com", 
          subject: "Build $BUILD_NUMBER for the $BRANCH_NAME branch passed.",
          body: "Successfully built acos branch $BRANCH_NAME build number $BUILD_NUMBER. Packages should be available at http://10.0.0.10/repositories/$BRANCH_NAME/$BUILD_NUMBER/index.html"
       )
    }
    failure {
       emailext (
          recipientProviders: [[$class: 'RequesterRecipientProvider']],
          to: "astepenko@aqueti.com",
          subject: 'FAILURE: build $BUILD_NUMBER of  ACOS branch $BRANCH_NAME',
          body: 'Failed to build acos branch $BRANCH_NAME build number $BUILD_NUMBER.')
    }   
  }
}
