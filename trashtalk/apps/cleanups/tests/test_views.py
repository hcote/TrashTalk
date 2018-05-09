import json

from django.utils.html import urlencode

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

    def test_api_cleanup_list_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_api_cleanup_create_view(self):
        cleanup = {
            'title': 'Test Cleanup Create',
            'description': 'A test event.',
            'start': '2018-04-15 15:30',
            'end': '2018-04-15 17:30',
            'location': {'number': '333',
                         'latitude': 123, 'longitude': 456,
                         'street': 'Beach Ave'}
        }
        self.client.force_login(self.user)
        response = self.client.post(self.url, data=json.dumps(cleanup),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_api_cleanup_update_success(self):
        cleanup = CleanupFactory(title='Oakland Test Cleanup', host=self.user)
        url = reverse('api:cleanup-detail', args=[cleanup.id])
        new_name = 'Oakland Cleanup'
        data = {'title': new_name,
                'description': cleanup.description,
                'host': self.user.id,
                'start': cleanup.start,
                'end': cleanup.end,
                'location': {'id': cleanup.location.id,
                             'number': '122',
                             'latitude': 123, 'longitude': 456,
                             'street': 'Sandy Lane'}
        }
        self.client.force_login(self.user)
        response = self.client.put(url, data=json.dumps(data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('title'), new_name)
        self.assertEqual(response.data.get('location')['number'], '122')

    def test_api_cleanup_patch_success(self):
        cleanup = CleanupFactory(description="An old description.", host=self.user)
        url = reverse('api:cleanup-detail', args=[cleanup.id])
        data = {'title': cleanup.title,
                'description': 'A new description.',
                'host': self.user.id}
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json.dumps(data),
                                     content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A new description.')

    def test_api_cleanup_change_participant_status(self):
        cleanup = CleanupFactory(title='Oakland Test Cleanup')
        url = reverse('api:cleanup-detail', kwargs={'pk': cleanup.id})
        added_data = {'participants': [self.user.id]}
        removed_data = {'participants': []}
        self.client.force_login(self.user)

        # Test participant was added
        response = self.client.patch(url, data=json.dumps(added_data), follow=True,
                                     content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user.id, response.data.get('participants'))

        # Test participant was removed
        response = self.client.patch(url, data=json.dumps(removed_data), follow=True,
                                     content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.user.id, response.data.get('participants'))

    def test_api_cleanup_delete_success(self):
        cleanup = CleanupFactory(title='Oakland Test Cleanup', host=self.user)
        url = reverse('api:cleanup-detail', args=[cleanup.id])
        data = {'id': cleanup.id}
        self.client.force_login(self.user)
        response = self.client.delete(url, data=json.dumps(data),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 204)
