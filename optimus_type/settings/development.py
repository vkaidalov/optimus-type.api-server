from .base import *  # noqa


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p(#03tt!#wmd(+pav5f&u&&4wc6c34+hno++3+q-)i&%v_vr6*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# django-cors-headers configuration
CORS_ORIGIN_ALLOW_ALL = True


# Needed for django-debug-toolbar
INTERNAL_IPS = [
    '127.0.0.1'
]
