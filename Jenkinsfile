#!/usr/bin/env groovy
import java.time.*

pipeline {
   agent any
   stages {
      stage('Checkout') {
         steps {
            checkout([$class: 'GitSCM', branches: [[name: '*/master']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[credentialsId: 'e5589e10-b755-49b0-8f64-b06df6ade600', url: 'https://github.com/Aqueti/acos.git']]])
//            sh "git submodule init"
//            sh "git submodule update"
//            echo "git clone git@github.com:Aqueti/acos.git"
//            sh "git clone git@github.com:Aqueti/acos.git"
         }
      }
      stage('Build') {
         steps {
            sh "mkdir -p build/acos"
            dir('build/acos') {
               sh "cmake ../.. -DBUILD_API:BOOL=ON -DBUILD_AGT:BOOL=ON -DBUILD_APPLICATIONS:BOOL=ON -DBUILD_TESTS:BOOL=ON -DBUILD_DEB_PACKAGE:BOOL=ON -DDOXYGEN_DIR:BOOL=~/Documentation"
               sh "make -j"
            }
         }
      }
      stage('Deploy') {
         steps {
            sh "Echo deploying..."
            sh "scp INSTALL/deb/* 192.168.0.1:\"/storage/Web/software\""
         }
      }
   }
}

