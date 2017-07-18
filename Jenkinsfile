#!/usr/bin/env groovy

pipeline {
   agent any
   stages {
      stage('Checkout') {
         steps {
            checkout([$class: 'GitSCM', branches: [[name: '*/master']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[credentialsId: 'e5589e10-b755-49b0-8f64-b06df6ade600', url: 'https://github.com/Aqueti/acos.git']]])
            sh "git submodule init"
            sh "git submodule update"
//            echo "git clone git@github.com:Aqueti/acos.git"
//            sh "git clone git@github.com:Aqueti/acos.git"
         }
      }
      stage('Build') {
         steps {
            sh "mkdir -p build/acos"
            dir('build/acos') {
               sh "cmake ../.. -DMAKE_API:BOOL=ON -DMAKE_AGT:BOOL=ON -DMAKE_APPLICATION:BOOL=ON -DMAKE_TESTS:BOOL=ON -DMAKE_DEB_PACKAGE:BOOL=ON -DDOXYGEN_DIR:BOOL=~/Documentation"
               sh "make -j"
            }
         }
      }
   }
}

