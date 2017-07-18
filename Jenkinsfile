#!/usr/bin/env groovy

pipeline {
   agent any
   stages {
      stage('Checkout') {
         steps {
            echo "git clone git@github.com:Aqueti/acos.git"
            sh "git clone git@github.com:Aqueti/acos.git"
         }
      }
      stage('Build') {
         steps {
            sh "mkdir -p build/acos"
            sh "cd build/acos; cmake ../../acos -DMAKE_API:BOOL=ON -DMAKE_AGT:BOOL=ON -DMAKE_APPLICATION:BOOL=ON -DMAKE_TESTS:BOOL=ON -DMAKE_DEB_PACKAGE:BOOL=ON -DDOXYGEN_DIR:BOOL=~/Documentation; make -j"
         }
      }
   }
}

