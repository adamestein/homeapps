from .dev import *

from library.testing.migrations import DisableMigrations

# Pytest uses its own settings module (see pytest.ini) so the 'test' in sys.argv branch of settings/__init__.py
# (which references the removed django_behave app) is never hit. Tests run against SQLite because the dev MySQL
# user has no permission to create the test_* database pytest-django needs.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/homeapps_test.sqlite3',
    }
}

DEBUG = False

# Speed up tests by skipping migrations and password hashing (django_plainpasswordhasher needs pkg_resources,
# which Python 3.13 removed, so use Django's built-in fast hasher instead)
MIGRATION_MODULES = DisableMigrations()
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']
