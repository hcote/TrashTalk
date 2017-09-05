from flask import Flask
from flask_login import LoginManager


app = Flask(__name__)

# Manage Login Feature
login_manager = LoginManager()
login_manager.init_app(app)

# Default configuration is development!
# Override with config.from_envvar('APP_ENV_VAR')
# http://flask.pocoo.org/docs/0.12/config/#configuring-from-files
app.config.from_object('trashtalk.settings.Development')

# Must import for views to load!
from trashtalk import views
