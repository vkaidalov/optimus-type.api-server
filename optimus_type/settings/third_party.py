import environ


env = environ.Env()


SHELL_PLUS_PRINT_SQL = env.bool('SHELL_PLUS_PRINT_SQL', default=False)

# Djoser settings

DJOSER = {
    'SERIALIZERS': {
        # Substituted in order to fix drf_yasg ref_name's collision.
        'user': 'users.serializers.AuthUserSerializer',
        'current_user': 'users.serializers.AuthUserSerializer',
    }
}

# DRF settings

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,

    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # TODO: Consider turning off this class.
        'rest_framework.authentication.SessionAuthentication',
    ),

    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),

    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer',
    ),

    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseFormParser',
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
    ),
}

# django-cors-headers settings

CORS_ORIGIN_ALLOW_ALL = True

# django-rest-framework-simplejwt settings

# TODO: Consider moving to JWT on frontend and configuring settings here.
SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
}

# drf-yasg settings

# TODO: Try to completely turn off session auth in Swagger UI.
SWAGGER_SETTINGS = {
    # 'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        # TODO: Repair this.
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}
