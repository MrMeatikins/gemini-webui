pipeline {
    agent {
        label 'aitop'
    }
    
    stages {
        stage('Initialize Build') {
            steps {
                // Initialize the deployment log and signal start
                sh """
                    echo '--- DEPLOYMENT STARTING #${env.BUILD_NUMBER} ---' > deployment.log
                    echo 'Build Number: ${env.BUILD_NUMBER}' >> deployment.log
                    echo "Deployment Started: \$(date)" >> deployment.log
                    cp deployment.log /tmp/jenkins-receipt-gemini-webui.log
                    sync
                """
            }
        }
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Deploy Gemini WebUI') {
            steps {
                script {
                    // Define credentials, but we'll handle missing ones gracefully
                    def creds = [
                        string(credentialsId: 'GOOGLE_API_KEY', variable: 'GEMINI_API_KEY'),
                        usernamePassword(credentialsId: 'ldap-bind-auth-user', passwordVariable: 'AD_BIND_PASS', usernameVariable: 'AD_BIND_USER_DN')
                    ]
                    
                    // Attempt to add the secret key if it exists
                    try {
                        creds << string(credentialsId: 'GEMINI_WEBUI_SECRET_KEY', variable: 'SECRET_KEY')
                    } catch (e) {
                        echo "Warning: GEMINI_WEBUI_SECRET_KEY not found, using a per-build random key."
                        env.SECRET_KEY = java.util.UUID.randomUUID().toString()
                    }

                    withCredentials(creds) {
                        env.ALLOWED_ORIGINS = "https://gemini.hackedyour.info"
                        sh 'docker compose down || true'
                        sh 'docker compose up --build -d'
                    }
                }
            }
        }
    }
    
    post {
        always {
            sh 'docker compose ps'
            withCredentials([string(credentialsId: 'Adam-Jenkins-Token', variable: 'ADAM_TOKEN')]) {
                sh """
                    curl -sL -u "adamoutler@gmail.com:${ADAM_TOKEN}" "${env.BUILD_URL}consoleText" > /tmp/jenkins-receipt-gemini-webui.log
                    echo "Finished: ${currentBuild.currentResult} #${env.BUILD_NUMBER}" >> /tmp/jenkins-receipt-gemini-webui.log
                """
            }
        }
    }
}