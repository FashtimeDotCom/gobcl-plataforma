# -*- coding: utf-8 -*-

import os

DEBUG = False

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
LOCAL_DATABASES = {
    'default': {
        # engines: 'postgresql', 'mysql', 'sqlite3' or 'oracle'
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'plataforma-gobcl',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

LOCALLY_INSTALLED_APPS = [
]

ENABLE_EMAILS = True

ADMINS = (())

LOCALLY_ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', [])
if LOCALLY_ALLOWED_HOSTS:
    LOCALLY_ALLOWED_HOSTS = LOCALLY_ALLOWED_HOSTS.split(',')

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = DEFAULT_FILE_STORAGE
THUMBNAIL_DEFAULT_STORAGE = DEFAULT_FILE_STORAGE
COMPRESS_STORAGE = DEFAULT_FILE_STORAGE
COMPRESS_URL = 'https://s3-us-west-2.amazonaws.com/gob.cl/'
STATIC_URL = COMPRESS_URL

CLAVE_UNICA_CALLBACK = 'https://gobcl.digital.gob.cl/callback'
CLAVE_UNICA_CLIENT_ID = 'c242172b23d349018620dae9d39fd8ee'
