#!/usr/bin/env groovy

pipeline {
   agent any
   stages {
      stage('Checkout') {
         steps {
            echo "git clone https://github.com/Aqueti/acos.git"
            git clone https://github.com/Aqueti/acos.git
         }
      }
      stage('Build') {
         steps {
            echo "Building..."
            mkdir -p build/acos
            cd build/acos
            cmake ../acos
            make -j
         }
      }
   }
}

