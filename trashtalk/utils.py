"""
geopy docs: https://wiki.openstreetmap.org/wiki/Nominatim

"""
import os
from collections import namedtuple

from geopy.exc import GeopyError, GeocoderQueryError, GeocoderParseError
from geopy.geocoders import Nominatim, GoogleV3

from flask import current_app

# ERROR HANDLING
# Add additional statuses as needed!
StatusCodes = namedtuple('StatusCodes', ['HTTP_200_OK', 'HTTP_201_CREATED',
                                         'HTTP_400_BAD_REQUEST', 'HTTP_403_FORBIDDEN',
                                         'HTTP_404_NOT_FOUND'])
status = StatusCodes(200, 201, 400, 403, 404)
geolocator = Nominatim()
google = GoogleV3(api_key=os.getenv('GOOGLE_MAPS_KEY'))
Point = namedtuple('Point', ['latitude', 'longitude'])

# RESPONSE OBJECTS
# Used to return nicely formatted, predictable data
Place = namedtuple('Place', ['name', 'number', 'street', 'district', 'city', 'county',
                             'state', 'zipcode', 'country', 'coordinates'])
Coordinates = namedtuple('Coordinates', ['latitude', 'longitude'])

# TOOLS
# Objects that require initialization for later use
geolocator = Nominatim()


def drop_db():
    """Delete all tables for this Metadata."""
    Base.metadata.drop_all()
    current_app.logger.info("Database tables dropped.")


def get_location(address):
    """
    Return full location data for given address. Requires a full address.

    Will not accept cross streets.

    :param street_number: `str`, Building number
    :param street_name: `str`
    :param city: `str`, Defaults to Oakland
    :return: `namedtuple`, `Place` with full location data
    """
    location=google.geocode(address)
    # print(location.address)
    # first_split=location.address.split(",")
    # street_split=first_split[0].split(" ")
    # zipcode_split=first_split[2].split(" ")

    return Place(address=location.address, latitude=location.latitude,
                 longitude=location.longitude)


    # try:
    #     res = geolocator.geocode(' '.join(address))
    # except (GeocoderQueryError, GeopyError):
    #     app.logger.exception("Geopy error.")
    #     raise
    # else:
    #     app.logger.info("Geolocator successful!: %s", address)
    #     print(res.address)
    #     location = res.address.split(',')
    #     if len(location) == 7:
    #         # Locations should only be of length 7 or 9
    #         # Handle for missing name and building number
    #         location.insert(0, None) * 2
    #     app.logger.info("Location: %s", location)
    #     return Place(name=location[0], number=location[1], street=location[2],
    #                  district=location[3], city=location[4], county=location[5],
    #                  state=location[6], zipcode=location[7], country=location[8],
    #                  latitude=res.latitude, longitude=res.longitude)

#
# def get_area(street_name, cross_street, city):
#     """
#     Return a generalized location area using cross streets. Google response:
#         Ex. 'Oakland, CA 94602, USA'
#
#
#     :param street_name:
#     :param cross_street:
#     :param city:
#     :return: `namedtuple`, with city, state, zipcode, country, lat and long
#     """
#     location = "{0}:{1} {2}".format(street_name, cross_street, city)
#     res = google.geocode(location)
#     print(res)
#     data = []
#     for item in res.address.split(','):
#         # Handle state and zipcode, which is returned in the format 'CA 94601'
#         if len(item.split()) > 1:
#             data.extend(item.split())
#         else:
#             data.append(item)
#     data = data.extend([res.latitude, res.longitude])
#     app.logger.info("Google Location: %s", data)
#
#     return Place(city=data[0], state=data[1], zipcode=data[2], country=data[3],
#                  latitude=data[4], longitude=data[5])

    # try:
    #     res = geolocator.geocode(' '.join(address))
    # except (GeocoderQueryError, GeopyError):
    #     app.logger.exception("Geopy error.")
    #     raise
    # else:
    #     app.logger.info("Geolocator successful!: %s", address)
    #     location = res.address.split(',')
    #     # FIXME: Response object is inconsistent. All fields not returned all the time.
    #     if len(location) == 7:
    #         # Locations should only be of length 7 or 9
    #         # Handle for missing name and building number
    #         location.insert(0, None) * 2
    #     app.logger.info("Location: %s", location)
    #     return Place(name=location[0], number=location[1], street=location[2],
    #                  district=location[3], city=location[4], county=location[5],
    #                  state=location[6], zipcode=location[7], country=location[8],
    #                  latitude=res.latitude, longitude=res.longitude)

    # try:
    #     res = geolocator.geocode(' '.join(address))
    # except (GeocoderQueryError, GeopyError):
    #     current_app.logger.exception("Geopy error.")
    #     raise
    # else:
    #     current_app.logger.info("Geolocator successful!: %s", address)
    #     location = res.address.split(',')
    #     coords = Coordinates(latitude=res.latitude, longitude=res.longitude)
    #     if len(location) == 7:
    #         # Locations should only be of length 7 or 9
    #         # Handle for missing name and building number
    #         location.insert(0, None) * 2
    #     current_app.logger.info("Location: %s", location)
    #     return Place(name=location[0], number=location[1], street=location[2],
    #                  district=location[3], city=location[4], county=location[5],
    #                  state=location[6], zipcode=location[7], country=location[8],
    #                  coordinates=coords)


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
    current_app.logger.info("Google Location: %s", data)

    return Place(city=data[0], state=data[1], zipcode=data[2], country=data[3],
                 latitude=data[4], longitude=data[5])
