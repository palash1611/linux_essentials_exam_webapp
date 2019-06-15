def app = 'Unknown'
pipeline {
    agent any
    stages {
        stage('build'){
            steps{
                script{
                    app = docker.build("palash1611/linux_exam_webapp")
                }
            }
        }
    }  
}
