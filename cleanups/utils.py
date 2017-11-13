"""
geopy docs: https://wiki.openstreetmap.org/wiki/Nominatim

"""
import logging
import os
from collections import namedtuple

from geopy.exc import GeopyError, GeocoderQueryError, GeocoderParseError
from geopy.geocoders import Nominatim, GoogleV3

from .constants import DEFAULT_CITY, DEFAULT_STATE

logger = logging.getLogger('cleanups.utils')

# ERROR HANDLING
# Add additional statuses as needed!
StatusCodes = namedtuple('StatusCodes', ['HTTP_200_OK', 'HTTP_201_CREATED',
                                         'HTTP_400_BAD_REQUEST', 'HTTP_403_FORBIDDEN',
                                         'HTTP_404_NOT_FOUND'])
status = StatusCodes(200, 201, 400, 403, 404)
geolocator = Nominatim()
google = GoogleV3(api_key=os.getenv('GOOGLE_MAPS_KEY'))

# RESPONSE OBJECTS
# Used to return nicely formatted, predictable data
Place = namedtuple('Place', ['name', 'number', 'street', 'district', 'city', 'county',
                             'state', 'zipcode', 'country', 'coordinates'])
Coordinates = namedtuple('Coordinates', ['latitude', 'longitude'])

# TOOLS
# Objects that require initialization for later use


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
        res = geolocator.geocode(address)
        coords = Coordinates(res.latitude, res.longitude)
    except (GeocoderQueryError, GeopyError):
        logger.exception("Geopy error: %s", address)
        raise
    else:
        logger.info("Geolocator successful!: %s", address)
        print(res.address)
        location = res.address.split(',')
        if len(location) == 7:
            # Locations should only be of length 7 or 9
            # Handle for missing name and building number
            logger.debug("Location: %s", location)
            return Place(name='', number='', street=location[0],
                         district=location[1], city=location[2], county=location[3],
                         state=location[4], zipcode=location[5], country=location[6],
                         coordinates=coords)

        logger.debug("Location: %s", location)
        return Place(name=location[0], number=location[1], street=location[2],
                     district=location[3], city=location[4], county=location[5],
                     state=location[6], zipcode=location[7], country=location[8],
                     coordinates=coords)


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
    logger.info("Google Location: %s", data)

    return Place(city=data[0], state=data[1], zipcode=data[2], country=data[3],
                 coordinates=(data[4], data[5]))


def get_full_address(request_form):
    selection = request_form['location']

    if selection == "current_address":
        full_address = request_form["current_address"]

    if selection =='cross_street':
        full_address=("%s at %s, %s, %s") % (request_form['street_one'],request_form['street_two'],DEFAULT_CITY, DEFAULT_STATE)

    if selection =='address':
        full_address = ("%s %s, %s, %s") % (request_form['street_number'], request_form['street_name'], DEFAULT_CITY, DEFAULT_STATE)

    return full_address


def check_participants(user, participants):
    participant_ids = []
    for participant in participants:
        participant_ids.append(participant.id)
    return user in participant_ids
