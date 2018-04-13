#!/usr/bin/env groovy

pipeline {    
  agent none
   
  options {
    timeout(time: 1, unit: 'HOURS')
  }

   stages {
      stage('Parallel build') {           
        failFast true
        parallel {
        stage('Render: build') {
          agent { label "compiler_1" }
          steps {            
            //git credentialsId: '', url: 'https://github.com/Aqueti/acos.git'
            
            stash includes: "release_notes.txt", name: 'release_notes'
            
            sh "mkdir -p jenkins/build/acos"
            dir('jenkins/build/acos') {
              sh "cmake ../../.. -DBUILD_API:BOOL=ON -DBUILD_AGT:BOOL=ON -DBUILD_APPLICATIONS:BOOL=ON -DBUILD_TESTS:BOOL=OFF -DBUILD_DEB_PACKAGE:BOOL=ON -DDOXYGEN_DIR:STRING=~/Documentation -DBUILD_AUTOFOCUS:BOOL=ON -DBUILD_OPENCV:BOOL=ON -DBUILD_EXAMPLES:BOOL=ON -DVERSION_TAG=${env.BRANCH_NAME} -DUSE_HTTPS:BOOL=OFF"
              sh "make -j"

              dir('INSTALL/deb') {
                stash includes: '*.deb', excludes: '*@*', name: 'acos'              
              }  
              dir('applications-prefix/src/applications-build/') { 
                sh 'make package'
                stash includes: '*.deb', excludes: '*@*', name: 'apps'          
              }
              dir('agt-prefix/src/agt-build/') {
                sh 'make package'
                stash includes: '*.deb', excludes: '*@*', name: 'agt'            
              }
            }
          }
          
          post {  
            always { 
              deleteDir()
            }
          }
        }
        
        stage('Render: test') {
          agent { label "compiler_1" }

          steps {           
            //git credentialsId: '', url: 'https://github.com/Aqueti/acos.git'
          
            sh "mkdir -p jenkins/build/acos"
            dir('jenkins/build/acos') {
               //Build acos and tests
               sh "cmake ../../.. -DBUILD_API:BOOL=ON -DBUILD_AGT:BOOL=ON -DBUILD_APPLICATIONS:BOOL=ON -DBUILD_TESTS:BOOL=ON -DBUILD_DEB_PACKAGE:BOOL=OFF -DUSE_DOXYGEN:BOOL=ON -DBUILD_AUTOFOCUS:BOOL=ON -DBUILD_OPENCV:BOOL=ON -DBUILD_EXAMPLES:BOOL=ON -DVERSION_TAG=${env.BRANCH_NAME} -DUSE_HTTPS:BOOL=OFF"
               sh "make -j"

               sh "./INSTALL/bin/testATL"

               dir('INSTALL') {
                sh "echo Looking for documentation at `pwd`"
                sh "tar -cvf Documentation.tar Documentation"
                stash includes:'Documentation.tar', name: 'documentation'
               }
            }
          }
          
          post {  
            always {                        
               deleteDir()
            }
          }
        }
        
        stage('Tegra: build') {
          agent { label "tegra_compiler_2" }
        
          steps {            
            //git credentialsId: '', url: 'https://github.com/Aqueti/acos.git'
              
            sh 'mkdir -p jenkins/build/acos'
            dir('jenkins/build/acos') {               
               sh "cmake ../../.. -DBUILD_API:BOOL=OFF -DBUILD_ACI:BOOL=ON -DBUILD_AGT:BOOL=OFF -DBUILD_APPLICATIONS:BOOL=OFF -DBUILD_TESTS:BOOL=OFF -DBUILD_DEB_PACKAGE:BOOL=OFF -DDOXYGEN_DIR:STRING=~/Documentation -DBUILD_AUTOFOCUS:BOOL=OFF -DBUILD_OPENCV:BOOL=OFF -DVERSION_TAG=${env.BRANCH_NAME} -DUSE_HTTPS:BOOL=OFF -DARGUS_INCLUDE_DIR:PATH=/usr/lib/aarch64-linux-gnu/tegra/"
               sh "make -j5"
            }
              
            dir('jenkins/build/acos') {
              sh "cmake ../../.. -DBUILD_API:BOOL=OFF -DBUILD_ACI:BOOL=ON -DBUILD_AGT:BOOL=OFF -DBUILD_APPLICATIONS:BOOL=OFF -DBUILD_TESTS:BOOL=OFF -DBUILD_DEB_PACKAGE:BOOL=ON -DDOXYGEN_DIR:STRING=~/Documentation -DBUILD_AUTOFOCUS:BOOL=OFF -DBUILD_OPENCV:BOOL=OFF -DVERSION_TAG=${env.BRANCH_NAME} -DUSE_HTTPS:BOOL=OFF -DARGUS_INCLUDE_DIR:PATH=/usr/lib/aarch64-linux-gnu/tegra/"
              sh "make -j5"
                
              dir('aci-prefix/src/aci-build') {
               sh "make package" 
               stash includes: '*.deb', excludes:'*@*', name: 'aci'               
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
     
      stage('Deploy') {
         agent { label 'master' }
         steps {                 
            echo "Deploy"
            
            sh "mkdir -p jkns"
            dir("jkns") {
                git credentialsId: '', url: 'https://github.com/Aqueti/jenkins.git'
            }
            
            sh "mkdir -p deploy/${env.BRANCH_NAME}/${env.BUILD_NUMBER}"
            dir("deploy/${env.BRANCH_NAME}/${env.BUILD_NUMBER}") {
               unstash 'acos'
               unstash 'agt'
               unstash 'apps'
               unstash 'aci'
               unstash 'release_notes'
              
               archiveArtifacts artifacts: '**/*.deb', fingerprint: true
               
               sh "../../../jkns/pipeline/bash/web_scr/genReleasePage.sh ${BRANCH_NAME} ${BUILD_NUMBER}"
               
               unstash 'documentation'
               sh "tar -xvf Documentation.tar"

               sh "../../../jkns/pipeline/bash/web_scr/genMainPage.sh ${BRANCH_NAME} ${BUILD_NUMBER}"
            }
            
            sh "rm -rf deploy"
            sh "rm -rf jkns"
         }
      } 

      stage('Build Tests') {
         agent { label 'cam_server_1' }
         steps {                 
            echo "Build Tests"
           
            unstash 'acos'
            unstash 'agt'
            unstash 'apps'
            unstash 'aci'
            
            sh "mkdir -p jkns"
            dir("jkns") {
                git credentialsId: '', url: 'https://github.com/Aqueti/jenkins.git'
            }
            
            dir("jkns/testScripts/apitest/") {
               sh "cmake ."
               sh "make -j"
            }
            
            sh 'jkns/pipeline/bash/run_scr/install.sh ${JOB_NAME} ${BRANCH_NAME}'
         }
      }

      stage('Run tests\nTX1') {
        agent { label 'cam_server_1' }
        steps {
          withEnv(['ENV_PATH="TX1"']) {
            sh 'jkns/pipeline/bash/run_scr/run.sh TX1 ${JOB_NAME} ${BRANCH_NAME}' 
          }
          
          junit '**/results.xml'
        }
      }
    
      stage('Run tests\nTX2') {
        agent { label 'cam_server_1' }
        steps {          
          withEnv(['ENV_PATH="TX2"']) {
            sh 'jkns/pipeline/bash/run_scr/run.sh TX2 ${JOB_NAME} ${BRANCH_NAME}' 
          } 
          
          junit '**/results.xml'
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
