from decouple import Csv, config

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="", cast=Csv())

CORS_ORIGIN_ALLOW_ALL = True

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT", default="", cast=int),
    },
}




# Paystack Integration
PAYSTACK_PUBLIC_KEY = (
    config("PAYSTACK_PUBLIC_KEY")
    if not config("DEV", cast=bool)
    else config("PAYSTACK_TEST_PUBIC_KEY")
)

PAYSTACK_SECRET_KEY = (
    config("PAYSTACK_SECRET_KEY")
    if not config("DEV", cast=bool)
    else config("PAYSTACK_TEST_SECRET_KEY")
)

PAYSTACK_PAYMENT_CALLBACK_URL = (
    config("PAYSTACK_PAYMENT_CALLBACK_URL")
    if not config("DEV", cast=bool)
    else config("PAYSTACK_TEST_PAYMENT_CALLBACK_URL")
)

PAYSTACK_BASE__URL = config("PAYSTACK_BASE__URL")






