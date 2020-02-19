from .base import *

DEBUG = True

ALLOWED_HOSTS = ['zookeeper.steinhome.net']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'homeapps5',
        'USER': 'homeapps',
        'PASSWORD': 'homeapps',
        'HOST': 'localhost',
        'OPTIONS': {
            'init_command': 'SET sql_mode="STRICT_ALL_TABLES"'
        }
    }
}

INSTALLED_APPS.append('django_extensions')
