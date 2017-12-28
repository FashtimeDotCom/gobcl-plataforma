# -*- coding: utf-8 -*-

DEBUG = True

LOCALLY_INSTALLED_APPS = [
]

ENABLE_EMAILS = True

LOCALLY_ALLOWED_HOSTS = []

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = DEFAULT_FILE_STORAGE
COMPRESS_STORAGE = DEFAULT_FILE_STORAGE
THUMBNAIL_DEFAULT_STORAGE = DEFAULT_FILE_STORAGE
# COMPRESS_URL = 'https://s3.amazonaws.com/gobcl-staging/'
COMPRESS_URL = 'https://s3-us-west-2.amazonaws.com/gob.cl/'
STATIC_URL = '/static/'

CLAVE_UNICA_CALLBACK = 'https://gobcl.magnet.cl/callback'
CLAVE_UNICA_CLIENT_ID = 'a73c92446de1481abf61c61fc2c5e091'
