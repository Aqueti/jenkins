#!/usr/bin/env groovy

pipeline {
   agent any
   stages {
      stage('Checkout') {
         steps {
            git clone https://github.com/Aqueti/acos.git
         }
      }
      stage('Build') {
         steps {
            echo "Building..."
            make -j
         }
      }
   }
}

