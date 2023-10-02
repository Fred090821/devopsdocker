pipeline {
    agent any
   options{
    //    buildDiscarder(logRotator(numToKeepStr:'20', daysToKeepStr:'5'))
          buildDiscarder(logRotator(numToKeepStr:'2', daysToKeepStr:'1'))
   }

    environment{
       HUB_REGISTRY_ID = 'adedo2009'
       IMAGE_NAME = 'devopsdocker'
       DOCKERHUB_CREDENTIALS = credentials('docker-hub')
       dockerImage = ''
   }

    stages {
        stage(' Verify Tooling ') {
            steps {
            echo '=== Verify Tooling ==='
                script {
                    try{
                        if (checkOs() == 'Windows') {
                            bat '''
                               docker version
                               docker info
                               python3 --version
                            '''
                        } else {
                            sh '''
                              docker version
                              docker info
                              python3 --version
                            '''
                        }
                    }catch(Exception e){
                        echo 'Exception Running Back End Server'
                        error('Aborting The Build')
                    }
                }
            }
        }
        stage(' Prune Docker Data ') {
            steps {
            echo '=== Prune Docker Data ==='
                script {
                    try{
                        if (checkOs() == 'Windows') {
                            bat '''
                               docker system prune -a -f
                               docker logout
                             '''
                        } else {
                            sh '''
                               docker system prune -a -f
                               docker logout
                             '''
                        }
                    }catch(Exception e){
                        echo 'Exception pruning the data'
                        error('Aborting The Build')
                    }
                }
            }
        }
         stage(' Checkout ') {
            steps {
            echo '=== Checkout Devops Code ==='
                script {
                    properties([pipelineTriggers([pollSCM('*/30 * * * *')])])
                }
                git 'https://github.com/Fred090821/devopsdocker.git'
            }
        }

        stage(' Start Rest Server...') {
            steps {
            echo '=== Start Back End Server ==='
                script {
                    try{
                        if (checkOs() == 'Windows') {
                            bat 'start/min /usr/bin/python3 rest_app.py'
                        } else {
                            sh 'nohup /usr/bin/python3 rest_app.py &'
                        }
                    }catch(Exception e){
                        echo 'Exception Running Back End Server'
                        error('Aborting The Build')
                    }
                }
            }
        }
        stage(' Run Rest Tests ') {
            steps {
            echo '=== Run Back End Tests ==='
                script {
                    try{
                        if (checkOs() == 'Windows') {
                            bat '/usr/bin/python3 backend_testing.py'
                        } else {
                            sh '/usr/bin/python3 backend_testing.py'
                        }
                    }catch(Exception e){
                        echo 'Exception Running Back End Test'
                        error('Aborting The Build')
                    }
                }
            }
        }
        stage(' Clean Environment ') {
            steps {
            echo '=== Clean Environment After Tests ==='
                script {
                    try{
                        if (checkOs() == 'Windows') {
                            bat '''
                               /usr/bin/python3 clean_environment.py
                             '''
                        } else {
                             sh '/usr/bin/python3 clean_environment.py'
                        }
                    }catch(Exception e){
                        echo 'Exception Cleaning The Environment'
                        error('Aborting The Build')
                    }
                }
            }
        }
        stage(' Docker Build Rest Image ') {
            steps {
                script {
                    try{
                        if (checkOs() == 'Windows') {
                           bat 'docker build -t $IMAGE_NAME .'
                        } else {
                            sh 'docker build -t $IMAGE_NAME .'
                        }
                    }catch(Exception e){
                        echo 'Exception Running Docker Build'
                        error('Aborting the build')
                    }
                }
            }
        }
        stage(' Log In To Docker hub ') {
            steps {
            echo '=== Log In To Docker hub ==='
                script {
                    try{
                        if (checkOs() == 'Windows') {
                            bat 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                        } else {
                            sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                        }
                    }catch(Exception e){
                        echo 'Exception Login into Ducker Hub'
                        error('Aborting The Build')
                    }
                }
            }
        }
        stage(' Tag & Push Rest Image ') {
            steps {
            echo '=== Tag & Push Rest Image ==='
                script {
                    try{
                        if (checkOs() == 'Windows') {
                            bat '''
                              docker tag $IMAGE_NAME $HUB_REGISTRY_ID/$IMAGE_NAME:latest
                              docker tag $IMAGE_NAME $HUB_REGISTRY_ID/$IMAGE_NAME:${BUILD_NUMBER}
                              docker push -a $HUB_REGISTRY_ID/$IMAGE_NAME
                            '''
                        } else {
                            sh '''
                              docker tag $IMAGE_NAME $HUB_REGISTRY_ID/$IMAGE_NAME:latest
                              docker tag $IMAGE_NAME $HUB_REGISTRY_ID/$IMAGE_NAME:${BUILD_NUMBER}
                              docker push -a $HUB_REGISTRY_ID/$IMAGE_NAME
                            '''
                        }
                    }catch(Exception e){
                        echo 'Exception Pushing Docker Build'
                        error('Aborting the build')
                    }
                }
            }
        }
    }
    post {
        always {
        echo '=== post Clean Environment ==='
            script {
                try{
                    if (checkOs() == 'Windows') {
                         bat '''
                              docker system prune -a -f
                              docker logout
                         '''
                    } else {
                         sh '''
                            docker system prune -a -f
                            docker logout
                         '''
                    }
                }catch(Exception e){
                        echo 'Exception docker compose starting container'
                        error('Aborting the build')
                }
            }
        }
        success {
            echo 'All test run successfully'
        }
        failure {
            echo 'One or more test(s) failed'
            emailext body: 'failed jenkins build', recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequestRecipientProvider']], subject: 'test'
        }
        unstable {
            echo 'The build is unstable'
        }
        changed {
            echo 'The pipeline  state has changed'
        }
    }
}

def checkOs(){
    if (isUnix()) {
        def uname = sh script: 'uname', returnStdout: true
        if (uname.startsWith("Darwin")) {
            return "Macos"
        }
        else {
            return "Linux"
        }
    }
    else {
        return "Windows"
    }

}

