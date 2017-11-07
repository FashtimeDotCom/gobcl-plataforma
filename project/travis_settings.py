# -*- coding: utf-8 -*-

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
