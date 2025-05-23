pipeline {
    agent any
    environment {
        AWS_DEFAULT_REGION = 'us-east-1'              // your AWS region
        S3_BUCKET = 'naveenkumarportfolio'       // your S3 bucket name
    }
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/Naveen-Kumar-Pikkili/Naveen-Portfolio.git'  // your Git repo URL
            }
        }
        stage('Deploy Frontend to S3') {
            steps {
                // Assuming your frontend files are in a folder called 'frontend'
                sh "aws s3 sync frontend/ s3://${S3_BUCKET} --delete"
            }
        }
        stage('Deploy Lambda Functions') {
            steps {
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
