from .local import *

INSTALLED_APPS = (
    'boh',
    'boh_api',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'widget_tweaks',

    'debug_toolbar',
)
