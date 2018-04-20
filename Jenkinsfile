pipeline {
  agent any
  stages {
    stage('Test') {
      steps {
        sh '''virtualenv venv --python=python3
. venv/bin/activate
pip install -U -r requirements/dev.txt
cp trashtalk/settings/dev.py.example trashtalk/settings/dev.py
mkdir logs
createdb trashtalk -U postgres
python manage.py migrate
python manage.py test apps'''
      }
    }
    stage('Merge') {
      steps {
        setGitHubPullRequestStatus(context: 'Tests done', message: 'tests done')
      }
    }
  }
}