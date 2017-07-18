#!groovy

//node{
//   echo "Hello from the Aqueti build pipeline! This is a linux machine"
//}

//build pipeline
pipeline {
   agent any

   stages {
      stage('BUILD') {
         steps {
            echo 'Building...'
         }
      }
      stage('UnitTest') {
         steps {
            echo 'Unit Testing...'
         }
      }
      stage('Deploy') {
         steps {
            echo 'Deploying...'
         }
      }
   }
}
