pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/zeninq/webapp.git'
            }
        }

        stage('Lint') {
            steps {
                echo "Skipping Python package installs — using Docker environment"
                sh """
                    docker run --rm \
                    -v \$(pwd)/app:/app \
                    python:3.11-slim \
                    sh -c "pip install flake8 && flake8 /app"
                """
            }
        }

        stage('Build images') {
            steps {
                sh "docker-compose build --no-cache"
            }
        }

        stage('Unit tests') {
            steps {
                sh """
                    docker-compose run --rm web pytest -q || true
                """
            }
        }

        stage('Containerized integration + Selenium tests') {
            steps {
                sh """
                    docker-compose up -d db web
                    sleep 8
                    docker-compose run --rm selenium_tests || true
                """
            }
        }
    }

    post {
        always {
            echo "---- COLLECTING LOGS ----"
            sh """
                mkdir -p jenkins_artifacts/logs
                docker-compose logs > jenkins_artifacts/logs/compose_logs.txt || true
            """
            archiveArtifacts artifacts: 'jenkins_artifacts/logs/**/*', allowEmptyArchive: true

            echo "---- CLEANUP ----"
            sh "docker-compose down -v || true"
        }
        failure {
            echo "Pipeline failed."
        }
    }
}
