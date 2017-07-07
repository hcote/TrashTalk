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
Place = namedtuple('Place', ['name', 'number', 'street', 'district', 'city', 'county', 'state', 'zipcode', 'country', 'latitude', 'longitude'])
Point = namedtuple('Point', ['latitude', 'longitude'])


def create_app(config):
    _app = Flask(__name__)
    app.config.from_envvar(config)

    return _app


def drop_db():
    """Delete all tables for this Metadata."""
    Base.metadata.drop_all()
    app.logger.info("Database tables dropped.")


def get_location(address):
    """
    Return full location data for given address. Requires a full address.

    Will not accept cross streets.

    :param street_number: `str`, Building number
    :param street_name: `str`
    :param city: `str`, Defaults to Oakland
    :return: `namedtuple`, `Place` with full location data
    """
    try:
        res = geolocator.geocode(' '.join(address))
    except (GeocoderQueryError, GeopyError):
        app.logger.exception("Geopy error.")
        raise
    else:
        app.logger.info("Geolocator successful!: %s", address)
        location = res.address.split(',')
        if len(location) == 7:
            # Locations should only be of length 7 or 9
            # Handle for missing name and building number
            location.insert(0, None) * 2
        app.logger.info("Location: %s", location)
        return Place(name=location[0], number=location[1], street=location[2],
                     district=location[3], city=location[4], county=location[5],
                     state=location[6], zipcode=location[7], country=location[8],
                     latitude=res.latitude, longitude=res.longitude)


def get_area(street_name, cross_street, city):
    """
    Return a generalized location area using cross streets. Google response:
        Ex. 'Oakland, CA 94602, USA'


    :param street_name:
    :param cross_street:
    :param city:
    :return: `namedtuple`, with city, state, zipcode, country, lat and long
    """
    location = "{0}:{1} {2}".format(street_name, cross_street, city)
    res = google.geocode(location)
    data = []
    for item in res.address.split(','):
        # Handle state and zipcode, which is returned in the format 'CA 94601'
        if len(item.split()) > 1:
            data.extend(item.split())
        else:
            data.append(item)
    data = data.extend([res.latitude, res.longitude])
    app.logger.info("Google Location: %s", data)

    return Place(city=data[0], state=data[1], zipcode=data[2], country=data[3],
                 latitude=data[4], longitude=data[5])
