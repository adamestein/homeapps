from base import *

DEBUG = True

ALLOWED_HOSTS = ['zookeeper.steinhome.net']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'homeapps',
        'USER': 'homeapps',
        'PASSWORD': 'homeapps',
        'HOST': 'localhost'
    }
}

INSTALLED_APPS.append('django_extensions')
