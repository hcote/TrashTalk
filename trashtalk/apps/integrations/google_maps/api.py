"""
Google Maps API
Package: https://github.com/google/google-api-python-client
Reference: https://googlemaps.github.io/google-maps-services-python/docs/
Geocoder: https://developers.google.com/maps/documentation/geocoding/start

"""
import logging
from collections import namedtuple

import googlemaps

from django.conf import settings

from core.exceptions import TrashTalkError

logger = logging.getLogger('integrations.google_maps.api')

Place = namedtuple('Place', ['number', 'street', 'district', 'city', 'county', 'state',
                             'country', 'zipcode', 'coordinates', 'place_id', 'categories'])
Coordinates = namedtuple('Coordinates', ['latitude', 'longitude'])


class GoogleMapsApi(object):

    def __init__(self, query=None):
        self.query = query  # Keep original query for error handling
        self.client = googlemaps.Client(key=settings.GOOGLE_API_KEY)

    def geocode(self, address):
        """
        Return a location given an address
        :param address: address, city, state
        :type address: string
        :return type: tuple Place
        """
        return GoogleAPIResponse(self.client.geocode(address), address).get_response()

    def reverse_geocode(self, coords):
        """
        Return a locations address given the coordinates.
        :param coords: `tuple` int lat, int long
        :return:
        """
        return GoogleAPIResponse(self.client.reverse_geocode(coords), coords)

    def place(self, place_id):
        """
        Return information about a specific place.

        :param place_id:
        :return:
        """
        return GoogleAPIResponse(self.client.place(place_id), place_id)

    def places(self, query, location):
        """
        Search for a place.

        Ex self.client.places('restaurant', 'Oakland, CA')
        :param query: `str` Search query
        :param location: `str, list, dict, tuple` The general area to search within
        :return:
        """
        return GoogleAPIResponse(self.client.places(query, location), (query, location,))

    def directions(self, origin, destination, mode='driving'):
        """
        Return directions given the origin and a destination.

        :param origin: `str` address or lat, long
        :param destination: `str` address or lat, long
        :param mode: `str` valid options are: transit, walking, driving, bicycling
        :return:
        """
        return GoogleAPIResponse(self.client.directions(origin, destination, mode=mode))


class GoogleAPIResponse:
    """
    Handles errors and data for Google Client responses for all search types.
    - Check for errors
    - Check the type of location returned: intersection, premise, street address

    Always returns a dictionary.
    """
    def __init__(self, response, query=None):
        self.query = query
        self.response = None
        self.status = None
        self.kind = []
        self._get_data(response)

    def _get_data(self, response):
        if not len(response) > 0:
            self.status = 400
            self.response = response
            return self.get_errors()
        else:
            self.response = response[0]
            self.status = 200
            self.kind = self.response['types']

    @property
    def is_intersection(self):
        return 'intersection' in self.kind

    def parse_intersection(self):
        streets = self.response['formatted_address'].split(',')[0]
        return Place(number='',
                     street=streets,
                     district=self.response['address_components'][1]['short_name'],
                     city=self.response['address_components'][2]['short_name'],
                     county=self.response['address_components'][3]['short_name'],
                     state=self.response['address_components'][4]['short_name'],
                     country=self.response['address_components'][5]['short_name'],
                     zipcode=self.response['address_components'][6]['short_name'],
                     coordinates=Coordinates(self.response['geometry']['location']['lat'],
                                             self.response['geometry']['location']['lng']),
                     place_id=self.response['place_id'],
                     categories=self.response['types'])

    def parse_address(self):
        return Place(number=self.response['address_components'][0]['short_name'],
                     street=self.response['address_components'][1]['short_name'],
                     district=self.response['address_components'][2]['short_name'],
                     city=self.response['address_components'][3]['short_name'],
                     county=self.response['address_components'][4]['short_name'],
                     state=self.response['address_components'][5]['short_name'],
                     country=self.response['address_components'][6]['short_name'],
                     zipcode=self.response['address_components'][7]['short_name'],
                     coordinates=Coordinates(self.response['geometry']['location']['lat'],
                                             self.response['geometry']['location']['lng']),
                     place_id=self.response['place_id'],
                     categories=self.response['types'])

    def get_response(self):
        """
        Return the correct data based on the kind of response.
        :return: Place
        :return type: `namedtuple`
        """
        if self.is_intersection:
            return self.parse_intersection()
        return self.parse_address()

    def get_errors(self):
        """Return a consistent response object."""
        raise TrashTalkError(message=self.query,
                             code='GOOGLE_API_ERROR',
                             base_exception=self.response)
