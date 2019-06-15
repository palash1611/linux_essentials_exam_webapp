def app = 'Unknown'
pipeline {
    agent any
    stages {
        stage('build'){
            steps{
                script{
                    app = docker.build("palash1611/linux_exam_webapp")
                    docker.withRegistry('', 'docker_hub'){
                        app.push("${env.BUILD_NUMBER}")
                    }
                }
            }
        }
    }  
}
