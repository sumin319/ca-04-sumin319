pipeline {
    agent { docker { image 'shahatuh/dp2306' } }

    environment {
        PATH = "env/bin/:$PATH"
    }
    stages {
        stage('build') {
            steps {
                sh 'python ca-04.py -q Images/queries/123600.ppm -s Images/search -m Hashtable -d 0'
                sh 'python ca-04.py -q Images/queries/123600.ppm -s Images/search -m List -d 0'
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'output/**/*.* ', onlyIfSuccessful: true
        }
    }
}
