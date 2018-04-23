"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

from importlib import import_module
import os
import sys

# django
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

PROJECT_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(PROJECT_DIR)

# local settings
if 'DOCKER' in os.environ:
    local_settings = import_module('project.production.local_settings')
elif 'STAGING' in os.environ:
    local_settings = import_module('project.staging.local_settings')
elif 'TRAVIS' in os.environ:
    local_settings = import_module('project.travis_settings')
else:
    local_settings = import_module('project.local_settings')


def get_local_value(key, default_value):
    try:
        return getattr(local_settings, key)
    except AttributeError:
        return default_value


ADMINS = local_settings.ADMINS
DEBUG = local_settings.DEBUG
ENABLE_EMAILS = local_settings.ENABLE_EMAILS
LOCALLY_ALLOWED_HOSTS = local_settings.LOCALLY_ALLOWED_HOSTS
LOCALLY_INSTALLED_APPS = local_settings.LOCALLY_INSTALLED_APPS

STATIC_URL = get_local_value('STATIC_URL', '/static/')
MEDIA_URL = get_local_value('MEDIA_URL', '/uploads/')
COMPRESS_URL = get_local_value('COMPRESS_URL', '/static/')
THUMBNAIL_DEFAULT_STORAGE = get_local_value(
    'THUMBNAIL_DEFAULT_STORAGE',
    'easy_thumbnails.storage.ThumbnailFileSystemStorage'
)
STATICFILES_STORAGE = get_local_value(
    'STATICFILES_STORAGE',
    'django.contrib.staticfiles.storage.StaticFilesStorage'
)
DEFAULT_FILE_STORAGE = get_local_value(
    'DEFAULT_FILE_STORAGE',
    'django.core.files.storage.FileSystemStorage'
)
COMPRESS_STORAGE = get_local_value(
    'COMPRESS_STORAGE',
    'compressor.storage.CompressorFileStorage'
)

CHILEATIENDE_ACCESS_TOKEN = get_local_value('CHILEATIENDE_ACCESS_TOKEN', '')


if DEBUG:
    env = 'development'
else:
    env = 'production'

# TEST should be true if we are running python tests
TEST = 'test' in sys.argv
TRAVIS = 'TRAVIS' in os.environ

# People who get code error notifications.
# In the format [
#     ('Full Name', 'email@example.com'),
#     ('Full Name', 'anotheremail@example.com'),
# ]
ADMINS = ADMINS

# List of IP addresses, as strings, that:
#   * See debug comments, when DEBUG is true
#   * Receive x-headers
INTERNAL_IPS = ['127.0.0.1', '10.0.2.2', ]

SECRET_KEY = os.getenv('SECRET_KEY', '=64Gh@&uwc7')

ALLOWED_HOSTS = [
    'gobcl.magnet.cl', 'localhost',
]

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
    'django.contrib.redirects',
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
    'django_cron',
    'adminsortable2',

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
    'services',
    'campaigns',
    'contingencies',
    'streams',
    'sociocultural_departments',
    'articles',

    # django cms
    'cms',
    'menus',
    'treebeard',
    'djangocms_text_ckeditor',
    'djangocms_link',
    'djangocms_video',
    'djangocms_picture',
    'djangocms_googlemap',
    'djangocms_snippet',
    'djangocms_style',
    'djangocms_file',
    'bootstrap4_grid',

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
    'gobcl_cms',

]

# Default email address to use for various automated correspondence from
# the site managers.
DEFAULT_FROM_EMAIL = 'no-reply@digital.gob.cl'
EMAIL_SENDER_NAME = 'GOBCL'

if DEBUG:
    INSTALLED_APPS += [
        'debug_toolbar',
    ]

    # Set the apps that are installed locally
    # only if we are on debug should we have locally installed apps
    INSTALLED_APPS = INSTALLED_APPS + LOCALLY_INSTALLED_APPS

MIDDLEWARE = [
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
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
    'gobcl_cms.middleware.increase_article_visits.IncreaseArticleVisits',
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
                'institutions.context_processors.get_most_visited_urls',
                'links.context_processors.footer_links',
                'base.context_processors.categories',
                'searches.context_processors.get_featured_news',
                'contingencies.context_processors.get_contingencies',
                'services.context_processors.get_chile_atiende_files',
                'project.context_processors.show_analytics_config',
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
    EMAIL_BACKEND = 'project.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'project.backends.smtp.EmailBackend'


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
    'eonasdan-bootstrap-datetimepicker': [
        'build/js/bootstrap-datetimepicker.min.js',
        'build/css/bootstrap-datetimepicker.min.css'
    ],
    '@gobdigital-cl': [
        'gob.cl/dist/js/gob.cl.js',
        'gob.cl/dist/fonts/*',
        'gob.cl/dist/images/*'
    ],
    'popper.js': ['dist/umd/popper.js'],
    'select2': [
        'dist/js/select2.full.js',
        'dist/css/select2.min.css'
    ],
    'slick-carousel': [
        'slick/slick.js',
        'slick/slick.min.js',
        'slick/slick.css',
        'slick/slick-theme.css',
        'slick/fonts/*',
        'slick/ajax-loader.gif'
    ],
    'magnific-popup': [
        'dist/jquery.magnific-popup.js',
        'dist/magnific-popup.css'
    ],
    'moment': [
        'moment.js',
        'locale/es.js',
        'min/moment-with-locales.min.js',
    ],
    'nprogress': ['nprogress.js'],
    'lodash': ['lodash.js']
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
        'debug_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '{}/logs/{}/clave_unica.log'.format(BASE_DIR, env),
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'debug_messages': {
            'handlers': ['debug_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
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
        'new_list_item': {'size': (495, 270), 'crop': True},
        'avatar': {'size': (328, 342), 'crop': True},
        'avatar_small': {'size': (218, 228), 'crop': True},
        'og_image': {'size': (1200, 630), 'crop': False},
        'image_home': {'size': (2500, 840), 'crop': True},
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
    ('campaigns/campaign_detail.pug', _('Campaign template')),
    ('empty.pug', _('Empty template')),
    ('streams/stream_detail.pug', _('Stream template')),
]

DJANGOCMS_STYLE_CHOICES = [
    'container',
    'container-fluid',
]

CMS_TOOLBARS = [
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

AWS_STORAGE_BUCKET_NAME = get_local_value('AWS_STORAGE_BUCKET_NAME', '')
AWS_S3_SECURE_URLS = True
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
AWS_S3_ENDPOINT_URL = os.getenv('AWS_S3_ENDPOINT_URL')
AWS_QUERYSTRING_AUTH = False
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')
COMPRESS_AUTOPREFIXER_BINARY = 'node_modules/postcss-cli/bin/postcss'
if get_local_value('AWS_S3_WITH_CUSTOM_DOMAIN', False):
    AWS_S3_HOST = AWS_STORAGE_BUCKET_NAME
    AWS_S3_CUSTOM_DOMAIN = AWS_S3_HOST

CLAVE_UNICA_SECRET_KEY = os.getenv('CLAVE_UNICA_SECRET_KEY', '')

PARLER_LANGUAGES = {
    1: (
        {
            'code': 'es',
            'fallbacks': ['en'],
        },
        {'code': 'en'},
    ),
    'default': {
        'fallback': 'es',
        'hide_untranslated': False,
    }
}

ELASTICSEARCH_DSL = {
    'HOST': get_local_value('ELASTICSEARCH_DSL_HOST', '127.0.0.1'),
    'PORT': get_local_value('ELASTICSEARCH_DSL_PORT', '9200'),
}

GOOGLE_OAUTH2_CLIENT_SECRETS_JSON = 'client_secrets.json'

CRON_CLASSES = (
    'services.cron.ChargeChileAtiendeServiceFile',
)

# Google Analytics API
GA_KEY_FILE_LOCATION = os.getenv('GA_KEY_FILE_LOCATION', '')
GA_SERVICE_ACCOUNT_EMAIL = os.getenv('GA_SERVICE_ACCOUNT_EMAIL', '')
GA_VIEW_ID = os.getenv('GA_VIEW_ID', '')


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '{}{}'.format(BASE_DIR, '/tmp/django_cache'),
    }
}

COMPRESS_OFFLINE = not DEBUG

SHOW_GOOGLE_ANALYTICS = get_local_value('SHOW_GOOGLE_ANALYTICS', False)
SHOW_HOTJAR = get_local_value('SHOW_HOTJAR', False)
SHOW_USABILLA = get_local_value('SHOW_USABILLA', False)


GOBCL_EMAIL_URL_SEND_EMAIL = get_local_value('GOBCL_EMAIL_URL_SEND_EMAIL', '')
GOBCL_EMAIL_ACCESS_URL = get_local_value('GOBCL_EMAIL_ACCESS_URL', '')
GOBCL_EMAIL_CLIENT_ID = get_local_value('GOBCL_EMAIL_CLIENT_ID', '')
GOBCL_EMAIL_CLIENT_SECRET = get_local_value('GOBCL_EMAIL_CLIENT_SECRET', '')
GOBCL_EMAIL_TOKEN_APP = get_local_value('GOBCL_EMAIL_TOKEN_APP', '')

CKEDITOR_SETTINGS = {
    'removeButtons': 'cmsplugins'
}
