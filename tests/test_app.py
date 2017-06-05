import pytest

from trashtalk import app


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
        response = client.get('/active_clean_ups')
        assert response.status_code == 200
