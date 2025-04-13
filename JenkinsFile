pipeline {
    agent any  // Use any available agent (node) to run the pipeline

    stages {
        stage('Checkout') {
            steps {
                // Checkout code from Git
                echo 'Cloning the Git repository...'
                git url: 'https://github.com/AkashUpadhyayy/mlops ', branch: 'main'
            }
        }
        
        stage('Verify Clone') {
            steps {
                // List the files in the workspace to verify that the code was cloned successfully
                echo 'Listing files in workspace...'
                sh 'ls -la'
            }
        }
    }
}
