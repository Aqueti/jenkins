#!groovy

node{
   echo "Hello from the Aqueti build pipeline! This is a linux machine"

}

//build pipeline
pipeline {
   agent any

   stages {
      stage('BUILD') {
         echo 'Building...'
      }
      stage('UnitTest') {
         echo 'Unit Testing...'
      }
      stage('Deploy') {
         echo 'Deploying...'
      }
   }
}
