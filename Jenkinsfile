pipeline {
    agent any

    environment {
        PATH = "/var/lib/jenkins/.local/bin:$PATH"
        DOCKER_IMAGE = "mt2024013/catvsdog"
        FRONTEND_DOCKER_IMAGE = "mt2024013/catvsdog-frontend"

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
                withCredentials([sshUserPrivateKey(credentialsId: 'my-repo-ssh-key', keyFileVariable: 'SSH_KEY')]) {
                    sh '''
                        # Setup Git user information
                        git config user.name "Akash Upadhyay"
                        git config user.email "akashupadhyay629@gmail.com"
                        
                        # Stage any changes including DVC meta files
                        git add .
                        
                        # Check if there are changes to commit
                        if git diff-index --quiet HEAD; then
                            echo "No changes to commit, skipping Git push"
                        else
                            # Commit and push changes
                            git commit -m "DVC: Updated data and models [skip ci]"
                            ssh-agent sh -c 'ssh-add $SSH_KEY; git push origin main'
                            echo "Changes committed and pushed successfully"
                        fi
                    '''
                }
            }
        }

        stage('Build Backend Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE}:latest ."
                }
            }
        }

        stage('Push Backend to Docker Hub') {
            steps {
                withDockerRegistry([credentialsId: 'docker-hub-credentials', url: '']) {
                    sh "docker push docker.io/${DOCKER_IMAGE}:latest"
                }
            }
        }
        
        stage('Build Frontend Docker Image') {
            steps {
                script {
                    sh '''
                        cd frontend
                        docker build -t ${FRONTEND_DOCKER_IMAGE}:latest .
                    '''
                }
            }
        }

        stage('Push Frontend to Docker Hub') {
            steps {
                withDockerRegistry([credentialsId: 'docker-hub-credentials', url: '']) {
                    sh "docker push docker.io/${FRONTEND_DOCKER_IMAGE}:latest"
                }
            }
        }

        stage('Deploy Using Ansible') {
            steps {
                sh '''
                    ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i inventory.ini ansible-playbook.yml
                '''
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    # Install Ansible Kubernetes collection if not already installed
                    ansible-galaxy collection install kubernetes.core

                    # Install Python kubernetes module if needed
                    pip install kubernetes>=12.0.0
                    
                    echo "==== Starting deployment of backend and frontend to Kubernetes ===="
                    
                    # Run the Kubernetes deployment playbook
                    ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i inventory.ini k8s-ansible-playbook.yml
                    
                    echo "==== Kubernetes deployment completed ===="
                '''
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
}