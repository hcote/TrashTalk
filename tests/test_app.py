import pytest

from trashtalk import app
from .factories import *


@pytest.fixture(scope='module')
def client():
    """
    `Fixture`_ to configure testing client for view requests.
    .. _link: https://docs.pytest.org/en/latest/builtin.html#fixtures-and-requests
    
    This automatically uses the (test) configuration settings for the TrashTalk app, but
    any additional configuration options should be added here.
    
    http://flask.pocoo.org/docs/0.12/config
    """
    app.testing = True
    app.config.from_object('trashtalk.settings.Testing')
    return app.test_client()


@pytest.mark.skip
@pytest.mark.usefixture('client')
class TestTrashTalkView:
    """
    Test public view responses.
    
    TODO: Setup template tests. 
    TODO: Parametrize and collapse endpoints into a single function.
    """

    def test_view_home_page(self, client):
        response = client.get('/')
        # client.add_template_test(fn, val)
        assert response.status_code == 200

    def test_view_signup(self, client):
        response = client.get('/signup')
        assert response.status_code == 200

    @pytest.mark.skip('FIXME: Database connection issues on test.')
    def test_view_cleanups(self, client):
        response = client.get('/cleanups')
        assert response.status_code == 200


@pytest.mark.skip
@pytest.mark.usefixture('client')
class TestUserLogin:
    """
    Tests that require database access.
    TODO: Setup test database.
    """

    def test_login(self, client):
        user = UserFactory(username='bigjoe', password='password')
        response = client.post('/login',
                               data={'username': user.username,
                                     'password': user.password})
        assert response.status_code == 200
        client.get('/logout')

    def test_unauthorized_user(self, client):
        response = client.get('/users')
        assert response.status_code == 403

    def test_signup_registration(self, client):
        response = client.post('/register', data={'username': 'test',
                                                        'password': 'password',
                                                        'confirm_password': 'password'})
        assert response.status_code == 201


@pytest.mark.skip
@pytest.mark.usefixture('client')
class TestUserView:
    """
    Authenticated views for logged in users.
    """
    def test_get_user_profile(self, client):
        user = UserFactory(username='bigjoe', password='password')
        url = '/profile/{}'.format(user.id)

        client.post('/login',
                    data={'username': user.username, 'password': user.password})
        response = client.get(url)
        assert response.status_code == 200
        # client.get('/logout')

    @pytest.mark.skip("Fix me.")
    def test_post_user_edit(self, client):
        user = UserFactory(username='bigjoe', password='password',
                           email='current_email@eample.com')
        login = client.post('/login',
                    data={'username': user.username,
                          'password': user.password})
        assert login.status_code == 200

        url = '/users/{}'.format(user.id)
        response = client.post(url, data={'method': 'PUT',
                                          'email': 'new_email@example.com'})
        assert response.status_code == 200
        assert user.email == 'new_email@example.com'

    def test_view_hosted_cleanups(self):
        pass

    def test_view_cleanups(self):
        pass

    def test_view_participating(self):
        pass


class CleanupViews:
    def test_view_cleanups(self):
        pass

    def test_view_cleanup_detail(self):
        pass

    def test_view_cleanup_delete(self):
        pass

    def test_view_cleanup_join(self):
        pass

    def test_view_cleanup_edit(self):
        pass


class SeeClickFix:
    """Separate into a test_seeclickfix.py"""
    pass

