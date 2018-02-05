"""
This is the settings file that you use when you're working on the project locally. Local development-specific settings
include DEBUG mode, log level, and activation of developer tools like django-debug-toolbar.
"""

from .base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['BOH_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['BOH_DB_NAME'],
        'USER': os.environ['BOH_DB_USER'],
        'PASSWORD': os.environ['BOH_DB_PASSWORD'],
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# Email
# https://docs.djangoproject.com/en/1.8/topics/email/#smtp-backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, os.pardir, os.pardir, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, os.pardir, os.pardir, 'media')


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ['BOH_SOCIAL_AUTH_GOOGLE_OAUTH2_KEY']
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ['BOH_SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET']
SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = ['mercari.com']
