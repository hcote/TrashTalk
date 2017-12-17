from datetime import date
from unittest import skip
from urllib.parse import urlencode

from django.test import TestCase
from django.urls import reverse

from cleanups.factories import *


class CleanupsAPIViewsTestCase(TestCase):
    def setUp(self):
        self.url = reverse('api:cleanups')
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
            'title': 'Cleanup Event 1',
            'description': 'A test event.',
            'start_time': '09:30 AM',
            'end_time': '11:30 AM',
            'date': date.today(),
            'number': '123',
            'street': 'Main Street',
            'host': self.user.id,
        }
        response = self.client.post(self.url, data=cleanup)

        self.assertEqual(response.status_code, 201)

    def test_cleanup_update_view(self):
        cleanup = CleanupFactory(title='Oakland Test Cleanup')
        url = reverse('api:cleanup-detail', args=[cleanup.id])
        new_name = 'Oakland Cleanup'
        data = urlencode({'title': new_name,
                          'description': cleanup.description,
                          'street': cleanup.location.street,
                          'number': cleanup.location.number,
                          'host': cleanup.host.id,
                          'date': date.today(),
                          'start_time': cleanup.start_time,
                          'end_time': cleanup.end_time})
        response = self.client.put(url, data=data,
                                   content_type='application/x-www-form-urlencoded')

        self.assertEqual(response.data.get('title'), new_name)

    def test_cleanup_add_participant(self):
        cleanup = CleanupFactory(title='Oakland Test Cleanup')
        url = reverse('api:join-cleanup', kwargs={'pk': cleanup.id})
        participant = UserFactory()
        data = urlencode({'participants': participant})
        response = self.client.patch(url, data=data,
                                     content_type='application/x-www-form-urlencoded')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(cleanup.participants.all()), 1)


class CleanupTemplateViewsTestCase(TestCase):
    def setUp(self):
        self.cleanup = CleanupFactory()
        CleanupFactory()
        CleanupFactory()

    def test_cleanup_edit_template(self):
        url = reverse('cleanup-edit', args=[self.cleanup.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_cleanup_list_template(self):
        url = reverse('cleanups-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_cleanup_new_template(self):
        url = reverse('cleanup-new')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
