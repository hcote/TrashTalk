import logging
import os

from trashtalk import app  # Shortcut to get around circular import


class Config(object):
    """
    Common configuration for all app instances and environments.
    Only add settings here which can be used in any environment.
    
    NEVER ADD SECRETS OR KEYS TO THIS SECTION.
    
    To use any Config object with Flask:
        - app.config.from_obj(path.to.config.Object)
    
    Configurations can further be over written by applying another config on top:
        - app.config.from_envvar(NAME_OF_ENV_VAR)
        - The ENV_VAR should be a path to a .cfg or .py file
    """

    DEBUG = False
    TESTING = False
    SECRET_KEY = 'do not add secret key'
    SESSION_COOKIE_NAME = 'trashtalk_session'

    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOGGING_LOCATION = 'trashtalk.log'
    LOGGING_LEVEL = logging.ERROR

    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'trashtalk')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(DB_USER,
                                                                            DB_PASSWORD,
                                                                            DB_HOST,
                                                                            DB_PORT,
                                                                            DB_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    GOOGLE_MAPS_KEY = os.getenv('GOOGLE_MAPS_KEY')
    GOOGLE_MAPS_ENDPOINT = "https://www.google.com/maps/embed/v1/place?key={0}" \
                           "&q=".format(GOOGLE_MAPS_KEY)


class Development(Config):
    """
    Settings specific to local development. You can use whatever database, settings and
    other tools and configure them here!
    
    It's OK to add keys or secrets which are only used for your local environment.
    """
    DEBUG = True
    LOGGING_LEVEL = logging.INFO


class Testing(Config):
    """
    Settings for testing.
    """
    TESTING = True
    LOGGING_LEVEL = logging.DEBUG

    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'trashtalk_test')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(DB_USER,
                                                                            DB_PASSWORD,
                                                                            DB_HOST,
                                                                            DB_PORT,
                                                                            DB_NAME)


class Production(Config):
    """
    Any settings should be set in the environment and requested  in this section.
    
    Example:
        SECRET_KEY = os.getenv('SECRET_KEY')
    """
    pass
