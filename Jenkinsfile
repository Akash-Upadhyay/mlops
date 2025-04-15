pipeline {
    agent any

    environment {
        PATH = "/var/lib/jenkins/.local/bin:$PATH"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Cloning the Git repository...'
                git url: 'https://github.com/Akash-Upadhyay/mlops.git', branch: 'main'
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                echo 'Setting up virtual environment...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install dvc
                '''
            }
        }

        stage('Verify Clone') {
            steps {
                echo 'Listing files in workspace...'
                sh 'ls -la'
            }
        }

        stage('DVC Pull') {
            steps {
                echo 'Pulling data and models from DVC remote...'
                withCredentials([file(credentialsId: 'dvc-gdrive-creds', variable: 'GDRIVE_CRED')]) {
                    sh '''
                        . venv/bin/activate
                        dvc remote modify gdrive_remote gdrive_use_service_account true
                        dvc remote modify --local gdrive_remote gdrive_service_account_json_file_path "$GDRIVE_CRED"
                        echo "GDRIVE_CRED: $GDRIVE_CRED"
                        dvc pull
                    '''
                }
            }
        }

        stage('DVC Reproduce') {
            steps {
                echo 'Reproducing the DVC pipeline...'
                sh '''
                    . venv/bin/activate
                    dvc repro
                '''
            }
        }
    }
}