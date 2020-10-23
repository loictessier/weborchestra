from . import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


SECRET_KEY = 'SERVER_SECRET_KEY'
DEBUG = False
ALLOWED_HOSTS = ['SITENAME', 'www.SITENAME']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'DB_NAME',
        'USER': 'DB_USER',
        'PASSWORD': 'DB_PASSWORD',
        'HOST': '',
        'PORT': '5432'
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'SERVER_EMAIL_HOST'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'SERVER_EMAIL_HOST_USER'
EMAIL_HOST_PASSWORD = 'SERVER_EMAIL_HOST_PASSWORD'

sentry_sdk.init(
    dsn="SENTRY_DSN_URL",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)
