from flask import Flask
from trashtalk.models import app, Base


def create_app(config):
    _app = Flask(__name__)
    app.config.from_envvar(config)

    return _app


def init_db():
    """
    Used to instantiate a new database. Must run from interpreter upon app setup!

    Import all modules here that might define models so that
    they will be registered properly on the metadata.  Otherwise
    you will have to import them first before calling init_db()

    :return: 
    """
    Base.metadata.create_all(bind=engine)
    app.logger.info("Database initialized.")


def drop_db():
    """Delete all tables for this Metadata."""
    Base.metadata.drop_all()
    app.logger.info("Database tables dropped.")
