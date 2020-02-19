import logging

from library.testing.migrations import DisableMigrations

# Turn off normal log messages (just leave CRITICAL in case it's something really bad)
logging.disable(logging.CRITICAL)

DEBUG = False

# No reason to go through migrations for the test database. If we are testing, we should have our models the way we
# want.
MIGRATION_MODULES = DisableMigrations()

# Speed up unit tests by avoiding password hashing
PASSWORD_HASHERS = ['django_plainpasswordhasher.PlainPasswordHasher']
