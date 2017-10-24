from flask import Flask
from werkzeug.utils import find_modules, import_string

from flask_login import LoginManager
from trashtalk.models import *

login_manager = LoginManager()


def app_factory(config_obj):
    """
    Create a new application instance.
    :param config_obj: `str` with dot notation (ex. 'app.settings.Production')
    :return: `Flask` app object
    """
    app = Flask(__name__)
    app.config.from_object(config_obj)

    # Initialize modules
    init_db(app)
    login_manager.init_app(app)

    # Register all blueprints
    register_all_blueprints(app)

    # Return application process
    return app


def register_all_blueprints(app):
    """
    Searches the Views directory for blueprints and registers them.

    All views must have a `bp` attribute whose value is a Blueprint(). Ex.:
        `bp = Blueprint('my_view', __name__)`

    It will not be registered with the current application unless it has
    this attribute!

    :param app: The application for registration
    :return:
    """
    for view in find_modules('trashtalk.views'):
        mod = import_string(view)
        uniq = set()
        if hasattr(mod, 'bp'):
            # Avoid duplicate imports
            if mod not in uniq:
                uniq.add(mod)
                app.register_blueprint(mod.bp)
    app.logger.info("Blueprints registered.")


def location_factory(data):
    location = Location(
        number=data.get('number').strip(),
        street=data.get('street').strip(),
        cross_street=data.get('cross_street'),
        city=data.get('city').strip(),
        state=data.get('state').strip(),
        zipcode=data.get('zipcode').strip(),
        county=data.get('county').strip(),
        district=data.get('district').strip(),
        country=data.get('country').strip(),
        latitude=data.get('latitude'),
        longitude=data.get('longitude')
    )
    location.save()
    return location


def cleanup_factory(data):
    cleanup = Cleanup(
        name=data.get('name'),
        description=data.get('description'),
        location=data.get('location'),
        date=data.get('date'),
        start_time=data.get('start_time'),
        end_time=data.get('end_time'),
        image=data.get('image'),
        host=data.get('host')
    )
    cleanup.save()
    return cleanup


def user_factory(**data):
    user = User(
        username=data.get('username'),
        password=data.get('password'),
        email=data.get('email')
    )
    user.save()
    return user
