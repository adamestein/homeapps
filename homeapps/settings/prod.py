from base import *

ALLOWED_HOSTS = ['.pythonanywhere.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'adamstein$default',
        'USER': 'adamstein',
        'PASSWORD': 'Uo96GnFjrwWtcCG',
        'HOST': 'adamstein.mysql.pythonanywhere-services.com',
        'OPTIONS': {
            'init_command': 'SET sql_mode="STRICT_ALL_TABLES"'
        }
    }
}

LOG_DIR = '/home/adamstein/logs'

# Logging handlers

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'django.log'),
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}
