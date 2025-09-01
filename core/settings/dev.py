from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']

REST_FRAMEWORK.update({
'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
})

INSTALLED_APPS += [
    'drf_spectacular',
]

DATABASES = {
    'default': env.db(
        'DATABASE_URL'
    )
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': False,
}
