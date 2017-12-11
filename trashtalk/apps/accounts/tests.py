from unittest import skip
from django.test import TestCase
from django.urls import reverse

from cleanups.factories import UserFactory, User


class UserAuthTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='loggyuser', password='password')
        UserFactory()

    def test_user_signup(self):
        url = reverse('api:users')
        user = {
            'username': 'FakeUser',
            'password': 'password',
            'password_confirmation': 'password',
            'email': 'faker@example.com'
        }

        response = self.client.post(url, data=user)

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

