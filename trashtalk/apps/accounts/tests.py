from unittest import skip
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode

from cleanups.factories import UserFactory, User, CleanupFactory


class UserAuthTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='loggyuser', password='password')
        UserFactory()

    @skip('Getting 415 errors ...')
    def test_user_signup(self):
        url = reverse('api:users-create')
        user = urlencode({
            'username': 'FakeUser',
            'password': 'password',
            'password_confirmation': 'password',
            'email': 'faker@example.com'
        })

        response = self.client.post(url, user,
                                    content_type='application/x-www-form-urlencoded')
        print(response.data)
        self.assertEqual(response.status_code, 201)

    @skip('May need to configure the request and session for this.')
    def test_user_login(self):
        user = User.objects.create_user(username='TestUser', password='password')
        login_data = {'username': user.username, 'password': user.password}

        is_logged_in = self.client.login(**login_data)
        self.assertTrue(is_logged_in)

    def test_user_login_template(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    @skip('Add login method for testing this.')
    def test_user_dashboard(self):
        url = reverse('dashboard')
        user = UserFactory()
        CleanupFactory(host=user)
        response = self.client.get(url, args=user.id)
        print(response.data)
        self.assertContains(response.data, 'cleanups')