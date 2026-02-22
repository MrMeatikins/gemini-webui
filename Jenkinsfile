pipeline {
    agent {
        label 'aitop'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Deploy Gemini WebUI') {
            steps {
                sh 'docker-compose down || true'
                sh 'docker-compose up --build -d'
            }
        }
    }
    
    post {
        always {
            sh 'docker-compose ps'
        }
    }
}