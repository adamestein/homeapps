"""
Base Django settings for homeapps project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Add the apps directory to the path since all code lives under there
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'apps')))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_#jzncdt0xc_%&*knkr5i=!*qesmi=pte7$a&lmw2jb34+n4kd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = DEBUG

from socket import gethostname
ALLOWED_HOSTS = [
    gethostname(),                          # For internal OpenShift load balancer security purposes.
    os.environ.get('OPENSHIFT_APP_DNS'),    # Dynamically map to the OpenShift gear name.
]

INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd Party Apps
    'easy_pdf',
    'south',
    'system_globals',
    'tekextensions',

    # Apps
    'finances',
    'library',
    'smoke_detectors',
    'utilities'
]

MIDDLEWARE_CLASSES = [
    # Django middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Home Apps middleware
    'library.middleware.save_requests.RequestMiddleware'
]

ROOT_URLCONF = 'homeapps.urls'

WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
# Set in dev.py or prod.py

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

# noinspection PyUnresolvedReferences
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', 'wsgi', 'static'))
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.normpath(os.path.join(BASE_DIR, '..', 'static'))
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Templates

TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]

TEMPLATE_CONTEXT_PROCESSORS = [
    # Django context processors
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.static',

    # 3rd Party processors
    'tekextensions.context_processors.static_url_prefix',

    # Home Apps context processors
    'finances.context_processors.bill_states',
    'library.context_processors.apps',
    'library.context_processors.version'
]

TEMPLATE_DIRS = [
    os.path.normpath(os.path.join(BASE_DIR, '..', 'templates'))
]

# Version information

VERSION = '3.0'
