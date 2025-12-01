pipeline {
  agent any

  environment {
    // change these if you want different image tags / registry
    WEB_IMAGE = "my-webapp_web:latest"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Lint') {
      steps {
        // install and run flake8; non-fatal by default (remove '|| true' to fail on lint)
        sh '''
          python3 -m pip install --user -r app/requirements.txt || true
          python3 -m pip install --user flake8 || true
          flake8 app || true
        '''
      }
    }

    stage('Build images') {
      steps {
        // build the web image and selenium test image
        sh 'docker compose build --pull --no-cache'
      }
    }

    stage('Unit tests') {
      steps {
        // Run unit tests in a one-off container using the web image.
        // This assumes pytest is in requirements.txt so it's available in the image.
        sh '''
          # bring up only db & web (detached)
          docker compose up -d db web
          # allow some time for DB init
          echo "Waiting for DB and web to be ready..."
          sleep 8
          # run pytest in an ephemeral container that shares the compose network
          docker compose run --rm web pytest -q || true
        '''
      }
    }

    stage('Containerized integration + Selenium tests') {
      steps {
        script {
          // run compose and return exit code; if non-zero, mark build failed
          def rc = sh(returnStatus: true, script: 'docker compose up --build --exit-code-from selenium_tests --abort-on-container-exit')
          if (rc != 0) {
            error "Selenium tests failed (exit code: ${rc})"
          }
        }
      }
    }
  }

  post {
    always {
      // collect logs and artifacts, then cleanup
      sh '''
        echo "---- CONTAINER PS ----"
        docker compose ps -a || true
        echo "---- COLLECTING LOGS ----"
        mkdir -p jenkins_artifacts/logs || true
        docker compose logs > jenkins_artifacts/logs/compose.log || true
        echo "---- CLEANUP ----"
        docker compose down -v --remove-orphans || true
      '''
      archiveArtifacts artifacts: 'jenkins_artifacts/**', allowEmptyArchive: true
    }
    success {
      echo "Pipeline finished successfully!"
    }
    failure {
      echo "Pipeline failed. Check logs/artifacts."
    }
  }
}
