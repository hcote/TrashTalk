import json
import os
from os.path import dirname, abspath

PROJECT_PATH = dirname(dirname(abspath(__file__)))


def get_credentials():
    """Return JSON object for Google API auth."""
    credentials = {
        "web": {
            "client_id": os.getenv('GOOGLE_CLIENT_ID'),
            "project_id": os.getenv('GOOGLE_PROJECT_ID'),
            "token_uri": os.getenv('GOOGLE_TOKEN_URI'),
            "auth_provider_x509_cert_url": os.getenv('GOOGLE_OAUTH_PROVIDER'),
            "client_secret": os.getenv('GOOGLE_CLIENT_SECRET'),
            "redirect_uris": os.getenv('GOOGLE_REDIRECT_URLS').split(','),   # a list []
            "javascript_origins": os.getenv('GOOGLE_JS_ORIGINS').split(',')  # a list []
        }
    }
    return json.dumps(credentials)
