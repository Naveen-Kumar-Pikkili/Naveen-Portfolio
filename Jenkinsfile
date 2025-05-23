pipeline {
    agent any
    environment {
        AWS_DEFAULT_REGION = 'us-east-1'           // Your AWS region
        S3_BUCKET = 'naveenkumarportfolio'         // Your S3 bucket name
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Naveen-Kumar-Pikkili/Naveen-Portfolio.git'
            }
        }
        stage('Deploy Frontend to S3') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-credentials'
                ]]) {
                    sh "aws s3 sync frontend/ s3://${S3_BUCKET} --delete"
                }
            }
        }
        stage('Deploy Lambda Functions') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-credentials'
                ]]) {
                    dir('lambda/contact') {
                        sh 'zip -r contact.zip *'
                        sh "aws lambda update-function-code --function-name ContactFormHandler --zip-file fileb://contact.zip"
                    }
                    dir('lambda/tracking') {
                        sh 'zip -r tracking.zip *'
                        sh "aws lambda update-function-code --function-name VisitorTrackingHandler --zip-file fileb://tracking.zip"
                    }
                }
            }
        }
    }
}
