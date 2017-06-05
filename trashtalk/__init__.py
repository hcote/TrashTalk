from flask import Flask

app = Flask(__name__)

# Default configuration is development!
# Override with config.from_envvar('APP_ENV_VAR')
# http://flask.pocoo.org/docs/0.12/config/#configuring-from-files
app.config.from_object('trashtalk.settings.Development')

# Must import for views to load!
from trashtalk import views
