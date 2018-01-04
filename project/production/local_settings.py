# -*- coding: utf-8 -*-
import os

DEBUG = False
LOCALLY_INSTALLED_APPS = []

ENABLE_EMAILS = True

ADMINS = (())

LOCALLY_ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', [])
if LOCALLY_ALLOWED_HOSTS:
    LOCALLY_ALLOWED_HOSTS = LOCALLY_ALLOWED_HOSTS.split(',')

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
THUMBNAIL_DEFAULT_STORAGE = DEFAULT_FILE_STORAGE
MEDIA_URL = 'https://s3-us-west-2.amazonaws.com/gob.cl/'
STATIC_URL = '/static/'

CLAVE_UNICA_CALLBACK = 'https://gobcl.digital.gob.cl/callback'
CLAVE_UNICA_CLIENT_ID = 'c242172b23d349018620dae9d39fd8ee'

# s3 static flies
COMPRESS_STORAGE = DEFAULT_FILE_STORAGE
COMPRESS_URL = MEDIA_URL
STATICFILES_STORAGE = DEFAULT_FILE_STORAGE

# override with local static files
COMPRESS_URL = '/static/'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
COMPRESS_STORAGE = STATICFILES_STORAGE
