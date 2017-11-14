"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import sys

# django
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

PROJECT_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(PROJECT_DIR)

# local settings
if 'TRAVIS' in os.environ:
    from project.travis_settings import DEBUG
    from project.travis_settings import LOCALLY_INSTALLED_APPS
    from project.travis_settings import ENABLE_EMAILS
    from project.travis_settings import ADMINS
elif 'DOCKER' in os.environ:
    from project.production.local_settings import DEBUG
    from project.production.local_settings import LOCALLY_INSTALLED_APPS
    from project.production.local_settings import ENABLE_EMAILS
    from project.production.local_settings import ADMINS
else:
    from project.local_settings import DEBUG
    from project.local_settings import LOCALLY_INSTALLED_APPS
    from project.local_settings import ENABLE_EMAILS
    from project.local_settings import ADMINS

if DEBUG:
    env = 'development'
else:
    env = 'production'

# TEST should be true if we are running python tests
TEST = 'test' in sys.argv

ADMINS = ADMINS


# List of IP addresses, as strings, that:
#   * See debug comments, when DEBUG is true
#   * Receive x-headers
INTERNAL_IPS = ['127.0.0.1', '10.0.2.2', ]

SECRET_KEY = os.getenv('SECRET_KEY', '=64Gh@&uwc7')

ALLOWED_HOSTS = [
    'gobcl.magnet.cl', 'localhost',
]

try:
    from project.local_settings import LOCALLY_ALLOWED_HOSTS
except:
    pass
else:
    ALLOWED_HOSTS += LOCALLY_ALLOWED_HOSTS

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'djangocms_admin_style',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    # external
    'compressor',
    'captcha',
    'loginas',
    'phonenumber_field',
    'filer',
    'easy_thumbnails',
    'mptt',
    'sekizai',
    'rest_framework',
    'django_filters',
    'hitcount',
    'haystack',
    'modeltranslation',

    # internal
    'base',
    'government_structures',
    'users',
    'public_servants',
    'ministries',
    'institutions',
    'regions',
    'presidencies',
    'links',
    'public_enterprises',
    'searches',

    # django cms
    'cms',
    'menus',
    'treebeard',
    'djangocms_text_ckeditor',
    'djangocms_link',
    'djangocms_video',
    'djangocms_googlemap',
    'djangocms_snippet',
    'djangocms_style',
    'djangocms_file',

    'aldryn_apphooks_config',
    'aldryn_categories',
    'aldryn_common',
    'aldryn_newsblog',
    'aldryn_people',
    'aldryn_reversion',
    'aldryn_translation_tools',
    'aldryn_search',
    'parler',
    'sortedm2m',
    'taggit',
    'reversion',

]

# Default email address to use for various automated correspondence from
# the site managers.
DEFAULT_FROM_EMAIL = 'no-reply@gob.cl'
EMAIL_SENDER_NAME = 'GOB'

if DEBUG:
    INSTALLED_APPS += [
        'debug_toolbar',
    ]

    # Set the apps that are installed locally
    # only if we are on debug should we have locally installed apps
    INSTALLED_APPS = INSTALLED_APPS + LOCALLY_INSTALLED_APPS

MIDDLEWARE = [
    'cms.middleware.utils.ApphookReloadMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'government_structures.middleware.get_current_government.GovernmentSetter',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
    'users.middleware.font_size.FontSizeMiddleware',
]

if DEBUG:
    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'sekizai.context_processors.sekizai',
                'cms.context_processors.cms_settings',
                (
                    'government_structures.context_processors.'
                    'add_government_structure_to_context'
                ),
                'institutions.context_processors.most_visited_urls',
                'links.context_processors.footer_links',
                'base.context_processors.categories',
                'searches.context_processors.get_feature_news',
            ],
            'loaders': [
                ('pypugjs.ext.django.Loader', (
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ))
            ],
            'builtins': ['pypugjs.ext.django.templatetags'],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME', 'plataforma-gobcl'),
        'USER': os.getenv('DB_USER', ''),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', ''),
        'PORT': os.getenv('DB_PORT', ''),
    }
}

# The email backend to use. For possible shortcuts see django.core.mail.
# The default is to use the SMTP backend.
# Third-party backends can be specified by providing a Python path
# to a module that defines an EmailBackend class.
if DEBUG or not ENABLE_EMAILS:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'UserAttributeSimilarityValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'MinimumLengthValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'CommonPasswordValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'NumericPasswordValidator'),
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'es'

LANGUAGES = (
    ('es', _('Spanish')),
    ('en', _('English')),
)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Santiago'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
LOCALE_PATHS = [
    PROJECT_DIR + '/locale'
]

USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static/')
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media/')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
    'npm.finders.NpmFinder',
)

##################
# AUTHENTICATION #
##################

AUTH_USER_MODEL = 'users.User'
LOGOUT_REDIRECT_URL = '/'

# set the precompilers
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
    ('text/pug', 'base.filters.pug.PugCompilerFilter'),
)

COMPRESS_CSS_FILTERS = [
    'django_compressor_autoprefixer.AutoprefixerFilter',
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]

LIBSASS_PRECISION = 10

# NPM
NPM_FILE_PATTERNS = {
    'bootstrap': ['dist/js/bootstrap.min.js'],
    'jquery': ['dist/jquery.min.js'],
    'moment': ['min/moment-with-locales.min.js'],
    'eonasdan-bootstrap-datetimepicker': [
        'build/js/bootstrap-datetimepicker.min.js',
        'build/css/bootstrap-datetimepicker.min.css'
    ],
    'gob.cl': [
        'dist/js/gob.cl.js',
        'dist/css/gob.cl.css',
        'dist/fonts/*',
        'dist/images/*'
    ],
    'popper.js': ['dist/umd/popper.js'],
    'select2': [
        'dist/js/select2.full.js',
        'dist/css/select2.min.css'
    ]
}

# default keys, replace with somethign your own
RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY', '')
RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY', '')
NOCAPTCHA = True
# un comment when we start using only SSL
# RECAPTCHA_USE_SSL = True
#
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'standard': {
            'format': (
                '%(asctime)s %(levelname)s: file %(filename)s line %(lineno)d '
                '%(message)s'
            )
        },
    },
    'handlers': {
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'formatter': 'standard',
            'level': 'ERROR',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': '{}/logs/{}/error.log'.format(BASE_DIR, env),
            'formatter': 'standard',
            'level': 'ERROR',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'file'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ]
}

if DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append(
        'rest_framework.renderers.BrowsableAPIRenderer',
    )

# ### Login as settings ###
CAN_LOGIN_AS = 'base.utils.can_loginas'
LOGOUT_URL = reverse_lazy('loginas-logout')
LOGINAS_LOGOUT_REDIRECT_URL = reverse_lazy('admin:index')

MOMMY_CUSTOM_CLASS = 'base.mommy.CustomMommy'

THUMBNAIL_ALIASES = {
    '': {
        'avatar': {'size': (218, 228), 'crop': True},
    },
}

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters'
)

THUMBNAIL_HIGH_RESOLUTION = True

# django cms
CMS_TEMPLATES = [
    ('base.pug', 'Home page template'),
]

DJANGOCMS_STYLE_CHOICES = [
    'container',
    'container-fluid',
]

CMS_TOOLBARS = [
    # CMS Toolbars
    'cms.cms_toolbars.PlaceholderToolbar',
    'cms.cms_toolbars.BasicToolbar',
    'cms.cms_toolbars.PageToolbar',

    # Aldryn newsblog toolbar
    'aldryn_newsblog.cms_toolbars.NewsBlogToolbar',
]

EMAIL_HOST = os.getenv('EMAIL_HOST', '')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
EMAIL_PORT = os.getenv('EMAIL_PORT', 587)
EMAIL_USE_TLS = True

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

ALDRYN_NEWSBLOG_SEARCH = False

AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME', '')
AWS_S3_SECURE_URLS = True
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
AWS_S3_CALLING_FORMAT_STATIC = os.getenv(
    'AWS_S3_CALLING_FORMAT_STATIC',
    'boto.s3.connection.SubdomainCallingFormat'
)
AWS_QUERYSTRING_AUTH = False
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')
STATIC_URL = os.getenv('STATIC_URL', '/static/')
MEDIA_URL = os.getenv('MEDIA_URL', '/uploads/')
DEFAULT_FILE_STORAGE = os.getenv(
    'DEFAULT_FILE_STORAGE',
    'django.core.files.storage.FileSystemStorage'
)
STATICFILES_STORAGE = os.getenv(
    'STATICFILES_STORAGE',
    'django.contrib.staticfiles.storage.StaticFilesStorage'
)
COMPRESS_URL = os.getenv('COMPRESS_URL', '/static/')
COMPRESS_STORAGE = os.getenv(
    'COMPRESS_STORAGE',
    'compressor.storage.CompressorFileStorage'
)
COMPRESS_AUTOPREFIXER_BINARY = 'node_modules/postcss-cli/bin/postcss'
