from unittest import skip

from django.test import TestCase
from django.urls import reverse

from cleanups.factories import *


class CleanupTestCase(TestCase):
    def setUp(self):
        self.url = reverse('cleanups-list')
        self.user = UserFactory()
        self.location = LocationFactory()
        CleanupFactory()
        CleanupFactory()
        CleanupFactory()

    @skip("Issue #83: Cleanup Api view test.")
    def test_cleanup_list_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    @skip("Issue #83: Cleanup Api view test.")
    def test_cleanup_create_view(self):
        cleanup = {
            'name': 'Cleanup Event 1',
            'description': 'A test event.',
            'start_time': '09:30 AM',
            'end_time': '11:30 AM',
            'host': self.user.id,
            'location': self.location.id
        }
        url = reverse('cleanup-create')
        response = self.client.post(self.url, data=cleanup)

        self.assertEqual(response.status_code, 201)
        cleanups = Cleanup.objects.all()
        self.assertEqual(len(cleanups), 4)

    @skip("Issue #83: Cleanup Api view test.")
    def test_cleanup_edit_view(self):
        cleanup = CleanupFactory(name='Oakland Test Cleanup')
        url = reverse('cleanup-edit', args=[cleanup.id])
        new_name = 'Oakland Cleanup'
        response = self.client.post(url, data={'name': new_name})

        self.assertEqual(response.data.get('name'), new_name )