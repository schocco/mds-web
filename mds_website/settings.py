# -*- coding: utf-8 -*-
# Django settings for mds_website project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_DIR = os.path.dirname(__file__)

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

#dont force trailing backslash
#APPEND_SLASH = False
#TASTYPIE_ALLOW_MISSING_SLASH = APPEND_SLASH

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.abspath(os.path.join(PROJECT_DIR, "media"))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.abspath(os.path.join(PROJECT_DIR, "../sitestatic"))

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.abspath(os.path.join(PROJECT_DIR, "static")),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Pipeline specific settings for JS and CSS compression
# yui-compressor is required, for a list of alternative compressors
# see https://django-pipeline.readthedocs.org/en/latest/compressors.html
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
PIPELINE_YUI_BINARY = "/usr/bin/yui-compressor"
PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.yui.YUICompressor'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.yui.YUICompressor'




PIPELINE_CSS = {
    'main': {
        'source_filenames': (
            'css/plugins.css',
            'css/workless.css',
            'css/typography.css',
            'css/font.css',
            'css/forms.css',
            'css/tables.css',
            'css/buttons.css',
            'css/alerts.css',
            'css/tabs.css',
            'css/pagination.css',
            'css/breadcrumbs.css',
            'css/helpers.css',
            'css/scaffolding.css',
            'css/print.css',
            'css/tooltip.css',
            'css/application.css',
        ),
        'output_filename': 'css/main.css',
    },
}
PIPELINE_JS = {
    'modernizer': {
        'source_filenames': (
          'js/modernizer/modernizer.js',
        ),
        'output_filename': 'js/modernizer.js',
    },
    'ie_font': {
        'source_filenames': (
          'js/ie_font.js',
        ),
        'output_filename': 'js/ie_font.js',
    },
    'jquery': {
        'source_filenames': (
          'js/jquery/jquery.js',
        ),
        'output_filename': 'js/jquery.js',
    },
    'main': {
        'source_filenames': (
          'js/jquery/plugins.js',
          'js/require/*.js',
          'js/underscore/*.js',
          'js/*.js',
          'js/app/models/*.js',
          'js/app/collections/*.js',
          'js/app/views/*.js',
          'js/app/*.js',
        ),
        'output_filename': 'js/main.js',
    },
    'require': {
        'source_filenames': (
          'js/require/require.js',
          'js/app/main.js',
        ),
        'output_filename': 'js/app/main.js',
    }
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'use your own secret key.'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mds_website.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'mds_website.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.gis',
    'south',
    'tastypie',
    'pipeline', #minify css and js
    'apps.muni_scales',
    'apps.trails',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'custom': {
            'handlers': ['console', 'mail_admins'],
            'level': 'DEBUG',
        }
    }
}

# import local settings file if one exists
# apparantly using system environments is the better solution
try:
    from settings_local import *
except Exception, e:
    print("Could not find a local settings file.")
