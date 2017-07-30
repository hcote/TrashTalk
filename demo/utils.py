from collections import namedtuple

from geopy.exc import GeopyError, GeocoderQueryError, GeocoderParseError
from geopy.geocoders import Nominatim, GoogleV3

from flask import Flask
from trashtalk.models import app

StatusCodes = namedtuple('StatusCodes', ['HTTP_200_OK', 'HTTP_201_CREATED',
                                        'HTTP_400_BAD_REQUEST', 'HTTP_403_FORBIDDEN', 'HTTP_404_NOT_FOUND'])
status = StatusCodes(200, 201, 400, 403, 404)
geolocator = Nominatim()
google = GoogleV3(api_key=app.config['GOOGLE_MAPS_KEY'])
Point = namedtuple('Point', ['latitude', 'longitude'])
Place = namedtuple('Place', ['address', 'latitude', 'longitude'])

def create_app(config):
    _app = Flask(__name__)
    app.config.from_envvar(config)

    return _app


def drop_db():
    """Delete all tables for this Metadata."""
    Base.metadata.drop_all()
    app.logger.info("Database tables dropped.")


def get_location(address_input):
    """
    Return full location data for given address. Requires a full address.

    Will not accept cross streets.

    :param street_number: `str`, Building number
    :param street_name: `str`
    :param city: `str`, Defaults to Oakland
    :return: `namedtuple`, `Place` with full location data
    """
    location=google.geocode(address_input)
    return Place(address=location.address, latitude=location.latitude,
                 longitude=location.longitude)


