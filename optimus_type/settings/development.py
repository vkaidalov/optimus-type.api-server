from .base import *


# Application definition

INSTALLED_APPS = INSTALLED_APPS + ['debug_toolbar']

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware'
] + MIDDLEWARE

# Required for django-debug-toolbar
INTERNAL_IPS = [
    '127.0.0.1'
]

# django-extensions shell_plus settings
SHELL_PLUS_PRINT_SQL = True

SECRET_KEY = 'p(#03tt!#wmd(+pav5f&u&&4wc6c34+hno++3+q-)i&%v_vr6*'

DEBUG = True

ALLOWED_HOSTS = ['*']


# django-cors-headers settings
CORS_ORIGIN_ALLOW_ALL = True
