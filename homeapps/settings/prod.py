from base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['OPENSHIFT_APP_NAME'],
        'USER': os.environ['OPENSHIFT_MYSQL_DB_USERNAME'],
        'PASSWORD': os.environ['OPENSHIFT_MYSQL_DB_PASSWORD'],
        'HOST': os.environ['OPENSHIFT_MYSQL_DB_HOST'],
        'PORT': os.environ['OPENSHIFT_MYSQL_DB_PORT']
    }
}
