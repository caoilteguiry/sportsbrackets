#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

import os
import django

# CG - Get a reference to DJANGO_ROOT and PROJECT_ROOT - will be useful later on
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

# Local time zone for this installation. 
TIME_ZONE = 'Europe/Dublin'

# Language code for this installation.
LANGUAGE_CODE = 'en-ie'

SITE_ID = 1

# Internationalisation and localisation
USE_I18N = True
USE_L10N = True


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

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
    'django.middleware.locale.LocaleMiddleware'
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
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
    'home',
    'user_profile',
)




LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'debugger': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}

# TODO: Should we really need to re-define the default values for this tuple here (i.e. django.co*)? It seems
# like a bad idea (the default values could change from version to version surely?).
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "custom_context_processors.site_prefs",
)

# see http://code.djangoproject.com/browser/django/trunk/django/conf/global_settings.py
gettext = lambda s: s

LANGUAGES = (
('en', gettext(u'English')),
('ga', gettext(u'Gaeilge')),
)



# Default page to redirect to if "next" input is not specified
LOGIN_REDIRECT_URL = "/"

# Lets handle CSRF failures ourself (instead of using  the default django error message). 
CSRF_FAILURE_VIEW = "error_handler.views.csrf_failure"

# Tell django where our extended user model lives (NB: This takes the form <app-name>.<model-name>,
# not <app-name>.<model-file-name>.<model-name> (e.g. user_profile.models.UserProfile), as one 
# might expect.
AUTH_PROFILE_MODULE = "user_profile.UserProfile"

LOGIN_URL = "/login"


# Unconventional django settings:
SITE_NAME = "Sports Ladders"

from settings_local import *
