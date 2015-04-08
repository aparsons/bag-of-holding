"""
Django settings for project project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

from django.contrib import messages

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ms+(*70s#y9f-6!1mmdof_e-z5t53&vh07$2si_76hahc&e-di'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'django_filters',
    'widget_tweaks',

    'boh',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'project.urls'

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Used for appending a site-wide prefix to all URLs. Example: 'boh/'
URL_PREFIX = ''

LOGIN_URL = os.path.join('/', URL_PREFIX, 'accounts/login')
LOGIN_REDIRECT_URL = os.path.join('/', URL_PREFIX)

# Changing error to danger for bootstrap compatibility
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = os.path.join('/', URL_PREFIX, 'static/')
MEDIA_URL = os.path.join('/', URL_PREFIX, 'media/')

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'boh/templates'),
)

# Development directories

if DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, os.pardir, 'static')
    MEDIA_ROOT = os.path.join(BASE_DIR, os.pardir, 'media')
    INSTALLED_APPS += (
        # 'debug_toolbar',
    )
