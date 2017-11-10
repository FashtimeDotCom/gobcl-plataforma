# -*- coding: utf-8 -*-

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

SECRET_KEY = '567ghsw%dshfoj)ty='
