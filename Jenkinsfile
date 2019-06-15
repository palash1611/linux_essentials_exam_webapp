pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building..'
		sh 'docker build -t palash1611/linux_exam_webapp:${BUILD_NUMBER}'
		sh 'docker push palash1611/linux_exam_webapp:${BUILD_NUMBER}'
            }
        }
    }
}
