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
         sh "mkdir -p build/acos"
         sh "cd build/acos; ccmake ../..; make -j"
      }
   }
}

