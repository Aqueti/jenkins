#!/usr/bin/env groovy

pipeline {
   agent any
   stages {
      stage('Download') {
         steps {
            echo "Downloading!"
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

