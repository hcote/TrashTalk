from unittest import skip

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
            'name': 'Cleanup Event 1',
            'description': 'A test event.',
            'start_time': '09:30 AM',
            'end_time': '11:30 AM',
            'host': self.user.id,
            'location': self.location.id
        }
        response = self.client.post(self.url, data=cleanup)

        self.assertEqual(response.status_code, 201)

    def test_cleanup_detail_view(self):
        cleanup = CleanupFactory(name='Oakland Test Cleanup')
        url = reverse('api:cleanup-detail', args=[cleanup.id])
        new_name = 'Oakland Cleanup'
        response = self.client.post(url, data={'name': new_name,
                                               'description': cleanup.description,
                                               'location': cleanup.location.id,
                                               'host': cleanup.host.id,
                                               'start_time': cleanup.start_time,
                                               'end_time': cleanup.end_time})

        self.assertEqual(response.data.get('name'), new_name)


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
