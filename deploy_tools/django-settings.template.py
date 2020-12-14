from . import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


DEBUG = False
ALLOWED_HOSTS = ['SITENAME', 'www.SITENAME']

## Server database settings

DATABASES = {
    'default': {
        'ENGINE': 'DB_ENGINE',
        'NAME': 'DB_NAME',
        'USER': 'DB_USER',
        'PASSWORD': 'DB_PASSWORD',
        'HOST': '',
        'PORT': 'DB_PORT'
    }
}

## Server email settings

EMAIL_BACKEND = 'SERVER_EMAIL_BACKEND'
EMAIL_HOST = 'SERVER_EMAIL_HOST'
EMAIL_USE_TLS = True
EMAIL_PORT = "SERVER_EMAIL_PORT"
EMAIL_HOST_USER = 'SERVER_EMAIL_HOST_USER'
EMAIL_HOST_PASSWORD = 'SERVER_EMAIL_HOST_PASSWORD'

## Sentry settings

sentry_sdk.init(
    dsn="SENTRY_DSN_URL",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

DEFAULT_FILE_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
DROPBOX_OAUTH2_TOKEN = os.environ.get('DROPBOX_OAUTH2_TOKEN')
DROPBOX_ROOT_PATH = '/'  # '/staging', '/prod'
