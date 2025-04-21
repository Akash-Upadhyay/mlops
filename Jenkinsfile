pipeline {
    agent any

    environment {
        PATH = "/var/lib/jenkins/.local/bin:$PATH"
        DOCKER_IMAGE = "mt2024013/catvsdog"
        BACKEND_IMAGE = "mt2024013/catvsdog"
        FRONTEND_IMAGE = "mt2024013/catvsdog-frontend"
    }

    stages {
        stage('Test SSH Connection') {
            steps {
                script {
                    node {
                        withCredentials([sshUserPrivateKey(credentialsId: 'my-repo-ssh-key', keyFileVariable: 'SSH_KEY')]) {
                            sh '''
                                ssh-agent sh -c 'ssh-add $SSH_KEY; ssh -T git@github.com || true'
                            '''
                        }
                    }
                }
            }
        }

        stage('Clone Repository') {
            steps {
                echo 'Cloning the Git repository...'
                checkout([$class: 'GitSCM', 
                    branches: [[name: '*/main']], 
                    userRemoteConfigs: [[
                        url: 'git@github.com:Akash-Upadhyay/mlops.git',
                        credentialsId: 'my-repo-ssh-key'
                    ]],
                    extensions: [[$class: 'LocalBranch', localBranch: 'main']]
                ])
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
                    dvc repro
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
                withCredentials([sshUserPrivateKey(credentialsId: 'my-repo-ssh-key', keyFileVariable: 'SSH_KEY')]) {
                    sh '''
                        # Setup Git user information
                        git config user.name "Akash Upadhyay"
                        git config user.email "akashupadhyay629@gmail.com"
                        
                        # Make some changes
                        echo "Update from Jenkins pipeline build 40" > jenkins_update.txt
                        
                        # Verify branch and status
                        git branch
                        git status
                        
                        # Stage and commit changes
                        git add -A
                        git diff-index --quiet HEAD || git commit -m "Automated commit from Jenkins"

                        
                        # Push changes using SSH
                        ssh-agent sh -c 'ssh-add $SSH_KEY; git push origin main'
                    '''
                }
            }
        }

        stage('Build Backend Docker Image') {
            steps {
                script {
                    sh "docker build -t ${BACKEND_IMAGE} ."
                }
                echo "Building Backend Docker Image..."
            }
        }

        stage('Push Backend to Docker Hub') {
            steps {
                withDockerRegistry([credentialsId: 'docker-hub-credentials', url: '']) {
                    sh "docker push docker.io/${BACKEND_IMAGE}"
                }
                echo "Pushing Backend to Docker Hub..."
            }
        }
        
        stage('Build Frontend Docker Image') {
            steps {
                script {
                    sh "docker build -t ${FRONTEND_IMAGE} -f frontend/Dockerfile frontend/"
                }
                echo "Building Frontend Docker Image..."
            }
        }

        stage('Push Frontend to Docker Hub') {
            steps {
                withDockerRegistry([credentialsId: 'docker-hub-credentials', url: '']) {
                    sh "docker push docker.io/${FRONTEND_IMAGE}"
                }
                echo "Pushing Frontend to Docker Hub..."
            }
        }
        
        stage('Deploy Using Ansible') {
            steps {
                sh '''
                    ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i inventory.ini ansible-playbook.yml
                '''
            }
        }
    }
}