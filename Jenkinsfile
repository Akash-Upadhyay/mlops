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
                    pip install dvc[gdrive]
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

        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies from requirements.txt...'
                sh '''
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('DVC Reproduce') {
            steps {
                echo 'Reproducing the DVC pipeline...'
                sh '''
                    . venv/bin/activate
                    #dvc repro
                '''
            }
        }

        stage('DVC Push') {
            steps {
                echo 'Pushing data and models to DVC remote...'
                withCredentials([file(credentialsId: 'dvc-gdrive-creds', variable: 'GDRIVE_CRED')]) {
                    sh '''
                        . venv/bin/activate
                        dvc remote modify gdrive_remote gdrive_use_service_account true
                        dvc remote modify --local gdrive_remote gdrive_service_account_json_file_path "$GDRIVE_CRED"
                        echo "GDRIVE_CRED: $GDRIVE_CRED"
                        dvc push
                    '''
                }
            }
        }

        stage('Git Push') {
            steps {
                echo 'Pushing changes to Git repository...'
                sshagent(['jenkins-ssh-key']) {
                    sh '''
                        . venv/bin/activate
                        git config user.name "Your Name"
                        git config user.email "your.email@example.com"
                        git add .
                        git commit -m "Update DVC files and code after training"
                        git push origin main
                    '''
                }
            }
        }
    }
}