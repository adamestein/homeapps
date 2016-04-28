from base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

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
