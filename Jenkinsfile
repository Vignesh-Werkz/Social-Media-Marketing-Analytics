void setBuildStatus(String message, String state) {
  step([
      $class: "GitHubCommitStatusSetter",
      reposSource: [$class: "ManuallyEnteredRepositorySource", url:"https://github.com/nus-cs3203/24s1-open-project-team03"],
      contextSource: [$class: "ManuallyEnteredCommitContextSource", context: "ci/jenkins/build-status"],
      errorHandlers: [[$class: "ChangingBuildStatusErrorHandler", result: "UNSTABLE"]],
      statusResultSource: [ $class: "ConditionalStatusResultSource", results: [[$class: "AnyBuildResult", message: message, state: state]] ]
  ]);
}


pipeline {
    agent any

    environment {
        GO_VERSION = '1.19'
        PYTHON_VERSION = '3.11'
    }

    triggers {
        githubPush()  // Trigger on every push event
    }

    stages {
        stage('Checkout') {
            steps { 
                checkout scm
            }
        }


        // stage('Set up Go') {
        //     steps {
        //         script {
        //             // Check if the required Go version is installed, and install if not
        //             sh '''
        //             if ! go version | grep -q "go${GO_VERSION}"; then
        //                 echo "Go ${GO_VERSION} not found, installing..."
        //                 curl -LO https://go.dev/dl/go${GO_VERSION}.linux-amd64.tar.gz
        //                 tar -C $HOME -xzf go${GO_VERSION}.linux-amd64.tar.gz
        //                 export PATH=$HOME/go/bin:$PATH
        //             else
        //                 echo "Go ${GO_VERSION} is already installed."
        //             fi

        //             # Ensure Go is in the PATH
        //             export PATH=$HOME/go/bin:$PATH
        //             go version
        //             '''
        //         }
        //     }
        // }

        // stage('Run Go Tests') {
        //     steps {
        //         script {
        //             sh 'go1.23.1 test ./...'
        //         }
        //     }
        // }

        stage('Set Up Python') {
            steps {
                script {
                    sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    . "$HOME/.cargo/env"
                    pip install -r requirements.txt
                    pip install coverage nltk
                    python3 -m nltk.downloader punkt punkt_tab
                    '''
                }
            }
        }
        
        stage('Run Python Tests with Coverage') {
            steps {
                script {
                    sh '''
                    . venv/bin/activate
                    python3 -m coverage run -m unittest
                    python3 -m coverage xml -o test/coverage.xml
                    '''
                }
            }
        }
    }

    post {
        success {
            setBuildStatus("Build succeeded", "SUCCESS");
        }
        failure {
            setBuildStatus("Build failed", "FAILURE");
        }

        always {
            // junit '**/test/*.xml'  // For Go or Python tests
            cobertura autoUpdateHealth: false, autoUpdateStability: false, coberturaReportFile: 'test/coverage.xml', conditionalCoverageTargets: '70, 0, 0'
            cleanWs()
        }
    }
}