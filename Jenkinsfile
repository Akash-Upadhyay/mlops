// pipeline {
//     agent any  // Use any available agent (node) to run the pipeline

//     environment {
//     PATH = "/var/lib/jenkins/.local/bin:$PATH"
//     }
//     stages {
//         stage('Checkout') {
//             steps {
//                 // Checkout code from Git
//                 echo 'Cloning the Git repository...'
//                 git url: 'https://github.com/AkashUpadhyayy/mlops ', branch: 'main'
//             }
//         }
        
//         stage('Verify Clone') {
//             steps {
//                 // List the files in the workspace to verify that the code was cloned successfully
//                 echo 'Listing files in workspace...'
//                 sh 'ls -la'
//             }
//         }
        
//         stage('DVC Pull') {
//             steps {
//                 // Pull data and models from DVC remote storage
//                 echo 'Pulling data and models from DVC remote...'
//                 sh 'dvc pull'
//             }
//         }
        
//         stage('DVC Reproduce') {
//             steps {
//                 // Reproduce the DVC pipeline
//                 echo 'Reproducing the DVC pipeline...'
//                 sh 'dvc repro'
//             }
//         }
//     }
// }


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

        stage('Verify Clone') {
            steps {
                echo 'Listing files in workspace...'
                sh 'ls -la'
            }
        }

        stage('DVC Pull') {
            steps {
                echo 'Pulling data and models from DVC remote...'
                // echo "GDRIVE_CRED: $GDRIVE_CRED"
                withCredentials([file(credentialsId: 'dvc-gdrive-creds', variable: 'GDRIVE_CRED')]) {
                    sh '''
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
                sh 'dvc repro'
            }
        }
    }
}
