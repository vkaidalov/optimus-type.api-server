import django_heroku

from .base import *


SECRET_KEY = get_env_value('SECRET_KEY')

DEBUG = False

CORS_ORIGIN_ALLOW_ALL = True

django_heroku.settings(locals(), test_runner=False)
