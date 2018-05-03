"""
DJANGO TRASHTALK SETTINGS
=========================

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

import os

from os.path import dirname

# =======================================================================
# SECURITY SETTINGS
# =======================================================================

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
DJANGO_ROOT = dirname(os.path.abspath(__file__))

# CURRENT PROJECT_DIR: trashtalk/trashtalk
PROJECT_DIR = dirname(DJANGO_ROOT)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: Configuration required for production!
# https://docs.djangoproject.com/en/1.11/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# =======================================================================
# APPLICATIONS
# On application start-up, Django looks for migrations files for each app
# =======================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps
    'accounts',
    'cleanups',
    'core',
    'integrations',

    # Tools
    'rest_framework',
    'gspread',
    'django_extensions',
    'raven.contrib.django.raven_compat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
]

# =======================================================================
# CONFIGURATION SETTINGS
# =======================================================================
ROOT_URLCONF = 'trashtalk.urls'
LOGIN_URL = '/login/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
            os.path.join(PROJECT_DIR, 'cleanups/templates'),
        ]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'trashtalk.wsgi.application'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

REST_FRAMEWORK_DOCS = {
    'HIDE_DOCS': True
}

# =======================================================================
# DATABASE SETTINGS
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
# =======================================================================

DATABASES = {
    'default': {}
}

# =======================================================================
# AUTHENTICATION
# =======================================================================
# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
AUTH_USER_MODEL = 'accounts.User'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# =======================================================================
# STATIC AND MEDIA
# https://docs.djangoproject.com/en/1.11/howto/static-files/
# You must run collectstatic to use STATIC_ROOT in staging and prod
# =======================================================================
STATIC_URL = '/assets/'
STATIC_ROOT = os.path.join(PROJECT_DIR, 'assets')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'uploads')

STATICFILES_DIRS = [
    # '/var/www/static/',
]

# =======================================================================
# FIXTURES
# https://docs.djangoproject.com/en/2.0/ref/settings/#std:setting-FIXTURE_DIRS
# =======================================================================
FIXTURE_DIRS = [
    os.path.join(PROJECT_DIR, 'fixtures')
]

# =======================================================================
# THIRD-PARTY INTEGRATION SETTINGS
# For settings specific to third-party modules and apis.
# The credentials below are NOT FOR PRODUCTION. Overwrite them by editing
# your dev.py
# =======================================================================

# See Click Fix Testing for all environments
SCF_HEADER = {"Content-type": "application/json"}
SCF_BASE_CALL = "https://test.seeclickfix.com/api/v2/issues"
SCF_ADMIN_USER = os.getenv("SCF_ADMIN_USER")
SCF_ADMIN_PASSWORD = os.getenv("SCF_ADMIN_PASSWORD")
SCF_CLEANUP_BASE_URL = os.getenv("SCF_CLEANUP_BASE_URL")

# =======================================================================
# LOGGING SETTINGS
# https://docs.djangoproject.com/en/1.11/topics/logging
# =======================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(dirname(PROJECT_DIR), 'logs', 'trashtalk.log'),
            'formatter': 'standard',
        },
        'file_sample': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PROJECT_DIR, 'logs', 'sample.log'),
            'formatter': 'standard',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True
        },
        'loggly': {
             'level': 'DEBUG',
             'class': 'logging.handlers.SysLogHandler',
             'facility': 'local7',
             'formatter': 'standard',
             'address': '/dev/log',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True,
        },
        'sample': {
            'handlers': ['file_sample'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'loggly_logs':{
             'handlers': ['loggly'],
             'level': 'DEBUG',
             'propagate': True,
        },
    }
}