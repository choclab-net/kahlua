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
        projectName   = 'kahlua'
        pythonVersion = '3.7'
        virtualEnv   = "${env.WORKSPACE}/venv"
        PATH          = "${virtualEnv}/bin:${PATH}"
        deployGit     = 'choclab-git'
        deployDev     = 'choclab-dev'
        deployProd    = 'choclab-prod'
        devServer     = 'galaxy.home.net'
        prodServer    = 'choclab.net'
        devUser       = "\$(awk '/^Host ${env.devServer}\$/{x=1}x&&/User/{print \$2;exit}' ~/.ssh/config)"
        prodUser      = "\$(awk '/^Host ${env.prodServer}\$/{x=1}x&&/User/{print \$2;exit}' ~/.ssh/config)"
    }

    stages {
        stage ('Install_Requirements') {
            steps {
                sh """[ -d venv ] && rm -rf venv
                    |python3 -m venv ${virtualEnv}
                    |source ${virtualEnv}/bin/activate
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
                    source ${virtualEnv}/bin/activate
                    make check || true
                """

                sh """
                    source ${virtualEnv}/bin/activate
                    { make flake8 | tee report/flake8.log; } || true
                """

                sh """
                    source ${virtualEnv}/bin/activate
                    { make bandit | tee report/bandit.log; } || true
                """

                sh """
                    source ${virtualEnv}/bin/activate
                    { make pylint | tee report/pylint.log; } || true
                """

                recordIssues(
                    enabledForFailure: true,
                    aggregatingResults: true,
                    tools: [pep8(), pyLint()]
                )
            }
        }

        stage ('Unit Tests') {
            steps {
                sh """
                    { make unittest; } || true
                """
            }

            post {
                always {
                    junit allowEmptyResults: true, keepLongStdio: true, testResults: 'report/nosetests.xml'
                    publishHTML target: [
                        reportDir: 'report/coverage',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report - Unit Test'
                    ]
                }
            }
        }

        stage ('Deploy develop') {
            when {
                branch 'develop'
            }
            steps {
                sshagent (credentials: [deployDev]) {
                    echo "Checking server for ${projectName} directory"
                    sh """
                    ssh ${devUser}@${devServer} -- '[ -d "${projectName}" ] || mkdir ${projectName}'
                    """

                    echo "Installing virtualenv"
                    sh """
                    |ssh -T ${devUser}@${devServer} <<'EOF'
                    |py_version=\$(
                    |    python3 -c "import sys; print('{}.{}'.format(sys.version_info[0], sys.version_info[1]))"
                    |)
                    |python3 -m venv virtualenv/${projectName}/\${py_version}
                    |EOF
                    |""".stripMargin()

                    echo "Transferring files"
                    sh """
                    files="\$(grep 'include\\|graft' MANIFEST.in | awk '{ print \$NF }') dev-requirements.txt"
                    scp -r \$files ${devUser}@${devServer}:${projectName}/
                    """

                    echo "Installing requirements"
                    sh """
                    |ssh -T ${devUser}@${devServer} <<'EOF'
                    |cd ${projectName}
                    |py_version=\$(
                    |    python3 -c "import sys; print('{}.{}'.format(sys.version_info[0], sys.version_info[1]))"
                    |)
                    |source ../virtualenv/${projectName}/\${py_version}/bin/activate
                    |pip install --upgrade pip
                    |pip install --upgrade -r requirements.txt -r dev-requirements.txt
                    |EOF
                    |""".stripMargin()

                    echo "Migrating database"
                    sh """
                    |ssh -T ${devUser}@${devServer} <<'EOF'
                    |cd ${projectName};
                    |py_version=\$(
                    |    python3 -c "import sys; print('{}.{}'.format(sys.version_info[0], sys.version_info[1]))"
                    |)
                    |source ../virtualenv/${projectName}/\${py_version}/bin/activate
                    |python manage.py makemigrations
                    |python manage.py migrate
                    |EOF
                    |""".stripMargin()

                    echo "Retrieving migrations"
                    sh """
                    scp -r ${devUser}@${devServer}:${projectName}/home/migrations/* home/migrations/
                    """

                    echo "Restarting site"
                    sh """
                    ssh ${devUser}@${devServer} -- 'sudo site ${projectName} restart'
                    """
                }

                echo "Checking for new migrations"
                sh """
                |if [ \$(git diff | wc -l) -ne 0 ]; then
                |    git checkout -b feature/migrations-\$(date +%Y%m%d%H%M)
                |    git add .
                !    git commit -m'Added automatic migration files'
                |else
                |    echo "No migrations to commit."
                |fi
                |""".stripMargin()

                sshagent([deployGit]) {
                    sh """
                    |REPO_URL=\$(git remote -v | grep -m1 '^origin' | sed -Ene's#.*(https://[^[:space:]]*).*#\\1#p')
                    |git remote set-url origin \$(
                    |    echo \${REPO_URL} |
                    |        sed -Ene's#https://github.com/([^/]*)/(.*).git#git@github.com:\\1/\\2.git#p'
                    |)
                    |git push origin \$(git rev-parse --abbrev-ref HEAD)
                    """.stripMargin()
                }
            }
        }

        // Selenium or behavioural tests should go once the site has deployed to development
        stage ('Integration and load tests tests') {
            when {
                branch 'develop'
            }
            steps {
                sh """
                make integration
                """

                sh """
                make load
                """
            }
        }

        stage ('Deploy production') {
            when {
                branch 'master'
            }
            steps {
                sshagent (credentials: [deployProd]) {
                    sh """
                    files="\$(grep 'include\\|graft' MANIFEST.in | awk '{ print \$NF }') passenger_wsgi.py"
                    scp -r \$files ${prodUser}@${prodServer}:${projectName}/
                    """

                    echo "Installing requirements"
                    sh """
                    |ssh -T ${prodUser}@${prodServer} <<'EOF'
                    |cd ${projectName}
                    |py_version='3.7'
                    |source ../virtualenv/${projectName}/\${py_version}/bin/activate
                    |pip install --upgrade pip
                    |pip install --upgrade -r requirements.txt -r dev-requirements.txt
                    |EOF
                    |""".stripMargin()

                    echo "Migrating database"
                    sh """
                    |ssh -T ${prodUser}@${prodServer} <<'EOF'
                    |py_version='3.7'
                    |source ../virtualenv/${projectName}/\${py_version}/bin/activate
                    |cd ${projectName}
                    |python manage.py migrate
                    |EOF
                    |""".stripMargin()
                }
            }
        }

        stage ('Smoke tests') {
            when {
                branch 'master'
            }
            steps {
                sh """
                make smoke
                """
            }
        }
    }
}
