"""
This is the settings file that you use when you're working on the project locally. Local development-specific settings
include DEBUG mode, log level, and activation of developer tools like django-debug-toolbar.
"""

from .base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5g3bqc$yp(+$obzr^z2=49grt%_ke5xp6i#5f$v17v7aldr!nr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
