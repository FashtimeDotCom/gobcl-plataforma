# -*- coding: utf-8 -*-

import os

DEBUG = True

# Database
LOCAL_DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'travis-gobcl',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

LOCALLY_INSTALLED_APPS = [
]

ENABLE_EMAILS = True

SECRET_KEY = 'TRAVIS'

ADMINS = (())

LOCALLY_ALLOWED_HOSTS = []

STATIC_URL = os.getenv('STATIC_URL', '/static/')
MEDIA_URL = os.getenv('MEDIA_URL', '/uploads/')
COMPRESS_URL = os.getenv('COMPRESS_URL', '/static/')
THUMBNAIL_DEFAULT_STORAGE = os.getenv(
    'THUMBNAIL_DEFAULT_STORAGE',
    'easy_thumbnails.storage.ThumbnailFileSystemStorage'
)
STATICFILES_STORAGE = os.getenv(
    'STATICFILES_STORAGE',
    'django.contrib.staticfiles.storage.StaticFilesStorage'
)
DEFAULT_FILE_STORAGE = os.getenv(
    'DEFAULT_FILE_STORAGE',
    'django.core.files.storage.FileSystemStorage'
)
COMPRESS_STORAGE = os.getenv(
    'COMPRESS_STORAGE',
    'compressor.storage.CompressorFileStorage'
)

CHILEATIENDE_ACCESS_TOKEN = os.getenv('CHILEATIENDE_ACCESS_TOKEN', '')
