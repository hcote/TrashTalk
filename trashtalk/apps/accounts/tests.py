from unittest import skip
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode

from cleanups.factories import UserFactory, User, CleanupFactory


class UserAuthTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='loggyuser', password='password')
        UserFactory()

    def test_user_signup(self):
        url = reverse('create-user')
        user = urlencode({
            'username': 'FakeUser',
            'password': 'Password1!',
            'confirm_password': 'Password1!',
            'email': 'faker@example.com'
        })

        response = self.client.post(url, user,
                                    content_type='application/x-www-form-urlencoded', follow=True)
        self.assertEqual(response.status_code, 200)

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