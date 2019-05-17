#!/usr/bin/env groovy

/**
 * Jenkinsfile
 */
pipeline {
    agent any
    options {
        buildDiscarder(
            logRotator(numToKeepStr:'10'))
    }
    environment {
        projectName = 'Kahlua'
        VIRTUAL_ENV = "${env.WORKSPACE}/venv"
        PATH="${VIRTUAL_ENV}/bin:${PATH}"
    }

    stages {
        stage ('Install_Requirements') {
            steps {
                sh """[ -d venv ] && rm -rf venv
                    |echo \$PATH
                    |python3 -m venv ${VIRTUAL_ENV}
                    |pip install --upgrade pip
                    |pip install -r requirements.txt -r dev-requirements.txt
                |""".stripMargin()
            }
        }

        stage ('Check_style') {
            steps {
                sh """
                    [ -d report ] || mkdir report
                """

                sh """
                    make check || true
                """

                sh """
                    { make flake8 | tee report/flake8.log; } || true
                """

                sh """
                    { make bandit | tee report/bandit.log; } || true
                """

                sh """
                    { make pylint | tee report/pylint.log; } || true
                """
                recordIssues(
                    enabledForFailure: true,
                    aggregatingResults: true,
                    tools: [pep8(), pylint()]
                )
            }
        }

        stage ('Unit Tests') {
            steps {
                sh """
                    make unittest || true
                """
            }

            post {
                always {
                    junit keepLongStdio: true, testResults: 'report/nosetests.xml'
                    publishHTML target: [
                        reportDir: 'report/coverage',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report - Unit Test'
                    ]
                }
            }
        }

        stage ('System Tests') {
            steps {
                sh """
                    make systest || true
                """
            }

            post {
                always {
                    junit keepLongStdio: true, testResults: 'report/nosetests.xml'
                    publishHTML target: [
                        reportDir: 'report/coverage',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report - System Test'
                    ]
                }
            }
        }

        stage ('Docs') {
            steps {
                sh """
                    PYTHONPATH=. pdoc --html --html-dir docs --overwrite env.projectName
                """
            }

            post {
                always {
                    publishHTML target: [
                        reportDir: 'docs/*',
                        reportFiles: 'index.html',
                        reportName: 'Module Documentation'
                    ]
                }
            }
        }
    }
}
