import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *
from .secret_key import SECRET_KEY


DEBUG = False
ALLOWED_HOSTS = ['intairemezzo-staging.fr', 'www.intairemezzo-staging.fr']

## Server database settings

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'intairemezzo_staging',
        'USER': get_env_variable('DB_USER'),
        'PASSWORD': get_env_variable('DB_PASSWORD'),
        'HOST': '',
        'PORT': '5432'
    }
}

## Server email settings

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = get_env_variable('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_HOST_PASSWORD')

## Sentry settings

sentry_sdk.init(
    dsn=get_env_variable('SENTRY_DSN_URL'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

DEFAULT_FILE_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
DROPBOX_OAUTH2_TOKEN = get_env_variable('DROPBOX_OAUTH2_TOKEN')
DROPBOX_ROOT_PATH = '/staging'
