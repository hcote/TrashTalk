from unittest import skip

from django.db import transaction
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

    def test_user_signup_validation(self):
        UserFactory(username='FakeUser')
        UserFactory(email='faker@example.com')
        url = reverse('create-user')
        user1 = urlencode({
            'username': 'FakeUser',
            'password': 'Password1!',
            'confirm_password': 'Password1!',
            'email': 'fakeuser@example.com'
        })
        user2 = urlencode({
            'username': 'FakeUser',
            'password': 'Password1!',
            'confirm_password': 'Password1!',
            'email': 'faker@example.com'
        })
        user3 = urlencode({
            'username': 'FakeUser',
            'password': 'firstpw!',
            'confirm_password': 'secondpw!',
            'email': 'faker@example.com'
        })

        # Testcases: duplicate email, duplicate username, password confirmation failed
        test_cases = [user1, user2, user3]
        for case in test_cases:
            # complete each DB transaction upon query fail to test the next query fail
            with transaction.atomic():
                response = self.client.post(url, case,
                                            content_type='application/x-www-form-urlencoded',
                                            follow=True)
                self.assertRedirects(response, reverse('register'))

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