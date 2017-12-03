from unittest import skip
from django.test import TestCase
from django.urls import reverse

from cleanups.factories import UserFactory, User


class UserAuthTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='loggyuser', password='password')
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

    @skip('Fix me')
    def test_user_login(self):
        login_url = reverse('login')
        login_data = {'username': self.user.username, 'password': self.user.password}

        response = self.client.post(login_url, login_data, follow=True)
        print(response.context)
        self.assertTrue(response.context['user'].is_authenticated())

    def test_user_login_template(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

