from unittest import skip
from django.test import TestCase

from integrations.google_maps.api import GoogleMapsApi


@skip("Fix Travis encrypted env variables to run this suite.")
class GoogleAPITestCase(TestCase):
    def setUp(self):
        self.google_client = GoogleMapsApi()

    def test_geocode_with_address_success(self):
        client = GoogleMapsApi()
        response = client.geocode('2323 Broadway, Oakland, CA')
        self.assertIsInstance(response, tuple)
        self.assertIn('premise', response.categories)

    def test_geocode_intersection_success(self):
        client = GoogleMapsApi()
        response = client.geocode('Fruitvale and MacArthur, Oakland, CA')
        self.assertIn('intersection', response.categories)
