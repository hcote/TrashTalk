"""
Trashtalk App
-------------

For more information, see README.md for the application. Default configuration is
Development.

Create Instance: See factories.py `app_factory` which contains init processes
Configuration: See settings.py for all configuration options and env variables
Running App: See run.py for all runtime options

"""
from flask import Flask
# from flask_login import LoginManager

from trashtalk.factories import app_factory


app = Flask(__name__)

# Manage Login Feature
# login_manager = LoginManager()
# login_manager.init_app(app)

# Default configuration is development!
# Override with config.from_envvar('APP_ENV_VAR')
# http://flask.pocoo.org/docs/0.12/config/#configuring-from-files
# app.config.from_object('trashtalk.settings.Development')
app = app_factory('trashtalk.settings.Development')
app.logger.info('Welcome to the Development server')
