from django.test import TestCase
from django.urls import reverse

from cleanups.factories import *


class CleanupTestCase(TestCase):
    def setUp(self):
        self.url = reverse('cleanups')
        self.user = UserFactory()
        self.location = LocationFactory()
        CleanupFactory()
        CleanupFactory()
        CleanupFactory()

    def test_cleanup_list_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_cleanup_create_view(self):
        cleanup = {
            'name': 'Cleanup Event 1',
            'description': 'A test event.',
            'start_time': '09:30 AM',
            'end_time': '11:30 AM',
            'host': self.user.id,
            'location': self.location.id
        }
        response = self.client.post(self.url, data=cleanup)

        self.assertEqual(response.status_code, 201)
        cleanups = Cleanup.objects.all()
        self.assertEqual(len(cleanups), 4)
