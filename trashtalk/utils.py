from collections import namedtuple
from flask import Flask
from trashtalk.models import app, Base

StatusCodes = namedtuple('StatusCodes', ['HTTP_200_OK', 'HTTP_201_CREATED',
                                        'HTTP_400_BAD_REQUEST', 'HTTP_403_FORBIDDEN', 'HTTP_404_NOT_FOUND'])
status = StatusCodes(200, 201, 400, 403, 404)


def create_app(config):
    _app = Flask(__name__)
    app.config.from_envvar(config)

    return _app


def drop_db():
    """Delete all tables for this Metadata."""
    Base.metadata.drop_all()
    app.logger.info("Database tables dropped.")
