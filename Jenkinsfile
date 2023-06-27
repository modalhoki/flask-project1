pipeline {
    agent any
    stages {
        stage('Delete the old container') {
            steps {
                echo 'Deleting old container'
                sh 'docker rm -f my-heart-prediction-testing2'
            }
        }

        stage('Delete unused image') {
            steps {
                echo 'Deleting unused images'
                sh 'docker image prune -a -f'
            }
        }

        stage('Build the image') {
            steps {
                echo 'Building the image'
                sh 'docker build -t ghcr.io/modalhoki/my-heart:heart-prediction-testing2 .'
            }
        }

        stage('Run the container') {
            steps {
                echo 'Running the container'
                sh 'docker run -d --name my-heart-prediction-testing2 -p 5000:5000 ghcr.io/modalhoki/my-heart:heart-prediction-testing2'
                sh 'docker update --restart always my-heart-prediction-testing2'
            }
        }

        stage('Check wether the container is running or not') {
            steps {
                echo 'Checking the container'
                sh 'docker ps'
            }
        }

        stage('Clear docker cache') {
            steps {
                echo 'Clearing docker cache'
                sh 'docker builder prune -a -f'
            }
        }
    }
}