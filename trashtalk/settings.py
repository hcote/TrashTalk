import logging
import os


class Config(object):
    """
    Common configuration for all app instances and environments.
    Only add settings here which can be used in any environment.

    NEVER ADD SECRETS OR KEYS TO THIS SECTION. Devs should use dev.cfg for customization.
    
    To use any Config object with Flask:
        - app.config.from_obj(path.to.config.Object)
    
    Configurations can further be over written by using instances or files:
        - app.config.from_envvar(NAME_OF_ENV_VAR)
        - The ENV_VAR should be a path to a .cfg or .py file
    """

    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'Not set')
    SESSION_COOKIE_NAME = 'trashtalk_session'
    SEE_ADMIN_USER = os.getenv('SCF_ADMIN_USER')

    # Logger Settings
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOGGING_LOCATION = 'trashtalk.log'
    LOGGING_LEVEL = logging.ERROR

    # Database Settings
    DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'trashtalk')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(DB_USER,
                                                                   DB_PASSWORD,
                                                                   DB_HOST,
                                                                   DB_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Google
    GOOGLE_MAPS_KEY = os.getenv('GOOGLE_MAPS_KEY')
    GOOGLE_MAPS_ENDPOINT = "https://www.google.com/maps/embed/v1/place?q="
    # GOOGLE_MAPS_ENDPOINT = "https://www.google.com/maps/embed/v1/place?key={0}" \
    #                        "&q=".format(GOOGLE_MAPS_KEY)
    GOOGLE_SHEETS_KEY = os.getenv('GOOGLE_SHEETS_KEY')
    GOOGLE_SHEETS_VALIDATION = os.getenv('GOOGLE_SHEETS_VALIDATION')

    # See Click Fix
    SCF_ADMIN_USER = os.getenv("SCF_ADMIN_USER")
    SCF_ADMIN_PASSWORD = os.getenv("SCF_ADMIN_PASSWORD")
    SCF_CLEANUP_BASE_URL = os.getenv("SCF_CLEANUP_BASE_URL")


class Development(Config):
    """
    Settings specific to local development. You can use whatever database, settings and
    other tools and configure them here!

    It's OK to add keys or secrets which are only used for your local environment.
    """
    DEBUG = True
    LOGGING_LEVEL = logging.INFO

    DB_HOST = os.getenv('DB_HOST', "")
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', "")
    DB_NAME = "trashtalk"


    # Access SQL
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(DB_USER,
                                                                   DB_PASSWORD,
                                                                   DB_HOST,
                                                                   DB_NAME)


class Testing(Config):
    """
    Settings for testing.
    """
    TESTING = True
    LOGGING_LEVEL = logging.DEBUG

    DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
    DB_USER = os.getenv('DB_USER', 'travis')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'trashtalk_test')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(DB_USER,
                                                                   DB_PASSWORD,
                                                                   DB_HOST,
                                                                   DB_NAME)


class Production(Config):
    """
    Any settings should be set in the environment and requested  in this section.

    Example:
        SECRET_KEY = os.getenv('SECRET_KEY')
    """
    DB_HOST = os.getenv('DB_HOST')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = "trashtalk"

    # Access SQL
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(DB_USER,
                                                                   DB_PASSWORD,
                                                                   DB_HOST,
                                                                   DB_NAME)
