import json

from datetime import date
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
            'start_time': '09:30 AM',
            'end_time': '11:30 AM',
            'date': str(date.today()),
            'host': self.user.id,
            'location': {'number': '333',
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
                'date': str(date.today()),
                'start_time': cleanup.start_time,
                'end_time': cleanup.end_time,
                'location': {'id': cleanup.location.id,
                             'number': '122',
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
        data = {'participants': [self.user.id]}
        self.client.force_login(self.user)

        # Test participant was added
        response = self.client.patch(url, data=json.dumps(data), follow=True,
                                     content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user.id, response.data.get('participants'))

        # Test participant was removed
        response = self.client.patch(url, data=json.dumps(data), follow=True,
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


class CleanupTemplateViewsTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.cleanup = CleanupFactory(host=self.user)
        CleanupFactory()
        CleanupFactory()

    def test_cleanup_list_template(self):
        url = reverse('cleanups-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_cleanup_new_template(self):
        url = reverse('cleanup-new')
        self.client.force_login(self.user)
        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, 200)

    def test_cleanup_create_success(self):
        url = reverse('cleanup-create')
        self.client.force_login(self.user)
        data = urlencode({'title': "New Cleanup Created",
                          'description': 'A totally new cleanup event!',
                          'number': '333',
                          'street': 'Newbie Ave',
                          'image': 'default.jpg',
                          'host': self.user,
                          'date': str(date.today()),
                          'start_time': '3:30 PM',
                          'end_time': '7:30 PM'})
        response = self.client.post(url, data=data,
                                    content_type='application/x-www-form-urlencoded')

        self.assertEqual(response.status_code, 200)

    def test_cleanup_edit_template(self):
        url = reverse('cleanup-edit', args=[self.cleanup.id])
        self.client.force_login(self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_cleanup_edit_success(self):
        url = reverse('cleanup-edit', args=[self.cleanup.id])
        self.client.force_login(self.user)
        data = {'title': "New Name Edited",
                'description': self.cleanup.description,
                'number': '122',
                'street': 'Sandy Lane',
                'host': self.user.id,
                'date': str(date.today()),
                'start_time': self.cleanup.start_time,
                'end_time': self.cleanup.end_time}
        response = self.client.put(url, data=data,
                                   content_type='application/x-www-form-urlencoded')

        self.assertEqual(response.status_code, 200)

    def test_cleanup_join_success(self):
        user = UserFactory()
        url = reverse('join-cleanup', args=[self.cleanup.id])
        data = urlencode({'participants': user.username})

        self.client.force_login(user)
        response = self.client.post(url, data=data,
                                    content_type='application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, 200)

    def test_cleanup_delete_success(self):
        cleanup = CleanupFactory(host=self.user)
        url = reverse('cleanup-delete', args=[cleanup.id])
        self.client.force_login(self.user)

        response = self.client.delete(url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('dashboard'))
