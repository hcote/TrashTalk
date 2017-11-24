"""
DJANGO TRASHTALK SETTINGS
=========================
These settings should be very carefully tested before changing them.

About Django Settings:
https://docs.djangoproject.com/en/1.11/topics/settings/

Deployment Checklist:
 https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

Settings is divided into several core sections:
- Security
- Installed Apps
- Django Config
- Database settings
- Auth
- Static and media
- Integration settings and credentials

More settings can be added at any time.
"""

from .common import *

# =======================================================================
# DEPLOYMENT SECURITY SETTINGS
# =======================================================================

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('TRASHTALK_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: Configuration required for production!
# https://docs.djangoproject.com/en/1.11/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['trashtalkdev.herokuapp.com']

# =======================================================================
# APPLICATIONS
# On application start-up, Django looks for migrations files for each app
# =======================================================================
INSTALLED_APPS += [
    # Any prod apps? Not likely ...
]

MIDDLEWARE += [
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

# =======================================================================
# CONFIGURATION SETTINGS
# =======================================================================

REST_FRAMEWORK_DOCS = {
    'HIDE_DOCS': os.getenv('HIDE_DRFDOCS', True)
}

# =======================================================================
# DATABASE SETTINGS
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
# =======================================================================
import dj_database_url

DATABASES = {
    'default': dj_database_url.config()
}

# =======================================================================
# AUTHENTICATION
# =======================================================================
# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS += []

# =======================================================================
# STATIC AND MEDIA
# https://docs.djangoproject.com/en/1.11/howto/static-files/
# =======================================================================
# STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# =======================================================================
# INTEGRATED APP SETTINGS
# Credentials and settings for integrated applications.
# =======================================================================

# GOOGLE MAPS -----------------------------------------------------------
GOOGLE_MAPS_KEY = os.getenv('GOOGLE_MAPS_KEY')
GOOGLE_MAPS_ENDPOINT = "https://www.google.com/maps/embed/v1/place?key={0}" \
                       "&q=".format(GOOGLE_MAPS_KEY)

# GOOGLE SHEETS ---------------------------------------------------------

# ID of spreadsheet found in Scope
GOOGLE_SHEETS_KEY = os.getenv('GOOGLE_SHEETS_KEY')

# Permission to access drive account
GOOGLE_SHEETS_VALIDATION = os.getenv('GOOGLE_SHEETS_VALIDATION')

# URL in Google Drive account to find spreadsheet
GOOGLE_SHEETS_SCOPE = ['https://spreadsheets.google.com/feeds/']

# SEE CLICK FIX ----------------------------------------------------------
