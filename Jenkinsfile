// pipeline {
//     agent any

//     environment {
//         PATH = "/var/lib/jenkins/.local/bin:$PATH"
//         BACKEND_IMAGE = "mt2024013/catvsdog"
//         FRONTEND_IMAGE = "mt2024013/catvsdog-frontend"
//     }

//     stages {
//         stage('Test SSH Connection') {
//             steps {
//                 script {
//                     node {
//                         withCredentials([sshUserPrivateKey(credentialsId: 'my-repo-ssh-key', keyFileVariable: 'SSH_KEY')]) {
//                             sh '''
//                                 ssh-agent sh -c 'ssh-add $SSH_KEY; ssh -T git@github.com || true'
//                             '''
//                         }
//                     }
//                 }
//             }
//         }

//         stage('Clone Repository') {
//             steps {
//                 echo 'Cloning the Git repository...'
//                 checkout([$class: 'GitSCM', 
//                     branches: [[name: '*/main']], 
//                     userRemoteConfigs: [[
//                         url: 'git@github.com:Akash-Upadhyay/mlops.git',
//                         credentialsId: 'my-repo-ssh-key'
//                     ]],
//                     extensions: [[$class: 'LocalBranch', localBranch: 'main']]
//                 ])
//             }
//         }

//         stage('Setup Virtual Environment') {
//             steps {
//                 echo 'Setting up virtual environment...'
//                 sh '''
//                     python3 -m venv venv
//                     . venv/bin/activate
//                     pip install --upgrade pip
//                     pip install dvc[gdrive]
//                 '''
//             }
//         }

//         stage('Verify Clone') {
//             steps {
//                 echo 'Listing files in workspace...'
//                 sh 'ls -la'
//             }
//         }

//         stage('DVC Pull') {
//             steps {
//                 echo 'Pulling data and models from DVC remote...'
//                 withCredentials([file(credentialsId: 'dvc-gdrive-creds', variable: 'GDRIVE_CRED')]) {
//                     sh '''
//                         . venv/bin/activate
//                         dvc remote modify gdrive_remote gdrive_use_service_account true
//                         dvc remote modify --local gdrive_remote gdrive_service_account_json_file_path "$GDRIVE_CRED"
//                         echo "GDRIVE_CRED: $GDRIVE_CRED"
//                         dvc pull
//                     '''
//                 }
//             }
//         }

//         stage('Install Dependencies') {
//             steps {
//                 echo 'Installing dependencies from requirements.txt...'
//                 sh '''
//                     . venv/bin/activate
//                     pip install -r requirements.txt
//                 '''
//             }
//         }

//         stage('DVC Reproduce') {
//             steps {
//                 echo 'Reproducing the DVC pipeline...'
//                 sh '''
//                     . venv/bin/activate
//                     dvc repro
//                 '''
//             }
//         }

//         stage('DVC Push') {
//             steps {
//                 echo 'Pushing data and models to DVC remote...'
//                 withCredentials([file(credentialsId: 'dvc-gdrive-creds', variable: 'GDRIVE_CRED')]) {
//                     sh '''
//                         . venv/bin/activate
//                         dvc remote modify gdrive_remote gdrive_use_service_account true
//                         dvc remote modify --local gdrive_remote gdrive_service_account_json_file_path "$GDRIVE_CRED"
//                         echo "GDRIVE_CRED: $GDRIVE_CRED"
//                         dvc push
//                     '''
//                 }
//             }
//         }

//         stage('Git Push') {
//             steps {
//                 echo 'Pushing changes to Git repository...'
//                 withCredentials([sshUserPrivateKey(credentialsId: 'my-repo-ssh-key', keyFileVariable: 'SSH_KEY')]) {
//                     sh '''
//                         # Setup Git user information
//                         git config user.name "Akash Upadhyay"
//                         git config user.email "akashupadhyay629@gmail.com"
                        
//                         # Make some changes
//                         echo "Update from Jenkins pipeline build 40" > jenkins_update.txt
                        
//                         # Verify branch and status
//                         git branch
//                         git status
                        
//                         # Stage and commit changes
//                         git add -A
//                         git diff-index --quiet HEAD || git commit -m "Automated commit from Jenkins"

                        
//                         # Push changes using SSH
//                         ssh-agent sh -c 'ssh-add $SSH_KEY; git push origin main'
//                     '''
//                 }
//             }
//         }

//         stage('Build Backend Docker Image') {
//             steps {
//                 script {
//                     sh "docker build -t ${BACKEND_IMAGE} ."
//                 }
//                 echo "Building Backend Docker Image..."
//             }
//         }

//         stage('Push Backend to Docker Hub') {
//             steps {
//                 withDockerRegistry([credentialsId: 'docker-hub-credentials', url: '']) {
//                     sh "docker push docker.io/${BACKEND_IMAGE}"
//                 }
//                 echo "Pushing Backend to Docker Hub..."
//             }
//         }
        
//         stage('Build Frontend Docker Image') {
//             steps {
//                 script {
//                     // Build the frontend image with the localhost and NodePort for backend service
//                     sh "docker build -t ${FRONTEND_IMAGE} --build-arg REACT_APP_API_URL=http://localhost:30800 -f frontend/Dockerfile frontend/"
//                 }
//                 echo "Building Frontend Docker Image for Kubernetes deployment with NodePort access..."
//             }
//         }

//         stage('Push Frontend to Docker Hub') {
//             steps {
//                 withDockerRegistry([credentialsId: 'docker-hub-credentials', url: '']) {
//                     sh "docker push docker.io/${FRONTEND_IMAGE}"
//                 }
//                 echo "Pushing Frontend to Docker Hub..."
//             }
//         }
        
//         stage('Deploy to Kubernetes') {
//             steps {
//                 sh '''
//                     # Ensure kubectl is installed
//                     which kubectl || { echo "kubectl not found, installing..."; apt-get update && apt-get install -y kubectl; }
                    
//                     # Create k8s directory if it doesn't exist
//                     mkdir -p k8s
                    
//                     # Create or overwrite the backend deployment file
//                     cat > k8s/backend-deployment.yaml << 'EOF'
// apiVersion: apps/v1
// kind: Deployment
// metadata:
//   name: catvsdog-backend
//   labels:
//     app: catvsdog
//     tier: backend
// spec:
//   replicas: 1
//   selector:
//     matchLabels:
//       app: catvsdog
//       tier: backend
//   template:
//     metadata:
//       labels:
//         app: catvsdog
//         tier: backend
//     spec:
//       containers:
//       - name: backend
//         image: mt2024013/catvsdog:latest
//         ports:
//         - containerPort: 8000
//         resources:
//           limits:
//             cpu: "1"
//             memory: "1Gi"
//           requests:
//             cpu: "500m"
//             memory: "512Mi"
// ---
// apiVersion: v1
// kind: Service
// metadata:
//   name: catvsdog-backend-service
//   labels:
//     app: catvsdog
//     tier: backend
// spec:
//   selector:
//     app: catvsdog
//     tier: backend
//   ports:
//   - port: 8000
//     targetPort: 8000
//   type: ClusterIP
// EOF

//                     # Create or overwrite the frontend deployment file
//                     cat > k8s/frontend-deployment.yaml << 'EOF'
// apiVersion: apps/v1
// kind: Deployment
// metadata:
//   name: catvsdog-frontend
//   labels:
//     app: catvsdog
//     tier: frontend
// spec:
//   replicas: 1
//   selector:
//     matchLabels:
//       app: catvsdog
//       tier: frontend
//   template:
//     metadata:
//       labels:
//         app: catvsdog
//         tier: frontend
//     spec:
//       containers:
//       - name: frontend
//         image: mt2024013/catvsdog-frontend:latest
//         ports:
//         - containerPort: 80
//         resources:
//           limits:
//             cpu: "500m"
//             memory: "512Mi"
//           requests:
//             cpu: "200m"
//             memory: "256Mi"
// ---
// apiVersion: v1
// kind: Service
// metadata:
//   name: catvsdog-frontend-service
//   labels:
//     app: catvsdog
//     tier: frontend
// spec:
//   selector:
//     app: catvsdog
//     tier: frontend
//   ports:
//   - port: 80
//     targetPort: 80
//   type: NodePort
// EOF

//                     # Fix kubectl configuration to avoid certificate issues
//                     kubectl config view
//                     CURRENT_CONTEXT=$(kubectl config current-context || echo "default")
//                     kubectl config set-context $CURRENT_CONTEXT --insecure-skip-tls-verify=true
//                     kubectl config unset "clusters.${CURRENT_CONTEXT}.certificate-authority" || true
//                     kubectl config unset "clusters.${CURRENT_CONTEXT}.certificate-authority-data" || true
                    
//                     # Fallback approach: Create a new, clean kubeconfig file if needed
//                     if ! kubectl apply -f k8s/backend-deployment.yaml; then
//                         echo "Trying fallback method with clean kubeconfig..."
//                         mkdir -p ~/.kube
//                         # Create a minimal kubeconfig file with only what's needed
//                         cat > ~/.kube/clean-config << EOF
// apiVersion: v1
// kind: Config
// clusters:
// - cluster:
//     insecure-skip-tls-verify: true
//     server: $(kubectl config view -o jsonpath='{.clusters[0].cluster.server}')
//   name: clean-cluster
// contexts:
// - context:
//     cluster: clean-cluster
//     user: clean-user
//   name: clean-context
// current-context: clean-context
// users:
// - name: clean-user
//   user: {}
// EOF
//                         # Try applying with the clean config
//                         KUBECONFIG=~/.kube/clean-config kubectl apply -f k8s/backend-deployment.yaml
//                         KUBECONFIG=~/.kube/clean-config kubectl apply -f k8s/frontend-deployment.yaml
                        
//                         # Use clean config for remaining commands
//                         export KUBECONFIG=~/.kube/clean-config
//                     else
//                         # Apply frontend if backend worked
//                         kubectl apply -f k8s/frontend-deployment.yaml
//                     fi
                    
//                     # Wait for deployments to be ready
//                     echo "Waiting for deployments to be ready..."
//                     kubectl rollout status deployment/catvsdog-backend
//                     kubectl rollout status deployment/catvsdog-frontend
                    
//                     # Get the frontend service NodePort and display it
//                     FRONTEND_PORT=$(kubectl get service catvsdog-frontend-service -o=jsonpath='{.spec.ports[0].nodePort}')
//                     echo "Frontend application is accessible at http://localhost:$FRONTEND_PORT"
//                 '''
//             }
//         }
//     }
// }

pipeline {
    agent any

    environment {
        PATH = "/var/lib/jenkins/.local/bin:$PATH"
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
                    // Build the frontend image with the localhost and NodePort for backend service
                    sh "docker build -t ${FRONTEND_IMAGE} --build-arg REACT_APP_API_URL=REACT_APP_API_URL=http://catvsdog.example.com/backend -f frontend/Dockerfile.k8s frontend/"
                }
                echo "Building Frontend Docker Image for Kubernetes deployment with NodePort access..."
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
        
        stage('Deploy to Kubernetes with Ansible') {
            steps {
                echo 'Deploying to Kubernetes with Ansible...'
                sh '''
                    # Install Ansible if not already installed
                    # which ansible-playbook || { echo "ansible-playbook not found, installing..."; apt-get update && apt-get install -y ansible; }
                    
                    # Run the Ansible playbook
                    ansible-playbook -i inventory.ini ansible-playbook.yml
                '''
            }
        }
        
    }
}