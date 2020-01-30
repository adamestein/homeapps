import os

if 'https_proxy' in os.environ:
    # Running on the PythonAnywhere production server
    from .prod import *
else:
    # Running on the dev server
    from .dev import *

# Default test runner for unit tests
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# If running test suite use any settings from tests.py
if 'test' in sys.argv or 'test_coverage' in sys.argv:
    testing = True

    try:
        from .testing import *
    except ImportError:
        pass

    # Use SQLite3 databases for testing instead of MySQL because:
    #
    #   o faster to start, faster to run, no cleanup needed
    #   o multiple tests can run at the same time
    #   o no need to 'destroy' the test database when starting a new test if the previous test
    #     stopped before cleaning up
    #
    # Need to set this here since tests.py will have no idea what DATABASES is.
    DATABASES["default"] = {'ENGINE': 'django.db.backends.sqlite3', 'NAME': '/tmp/default.db'}

    # Set up so that we can run BDD tests. We use the Django Behave test runner so that we can run our normal unit
    # tests in addition to the BDD tests.
    INSTALLED_APPS += ('django_behave', )

    if '--unit-tests-only' in sys.argv:
        # Don't change Django's default test runner so only Django unit tests will run
        del sys.argv[sys.argv.index('--unit-tests-only')]
    elif '--bdd-tests-only' in sys.argv:
        # Set up test runner to ONLY run bdd tests
        TEST_RUNNER = 'django_behave.runner.DjangoBehaveOnlyTestSuiteRunner'
        del sys.argv[sys.argv.index('--bdd-tests-only')]
    else:
        # Set up test runner to run both normal Django unit tests AND bdd tests
        TEST_RUNNER = 'django_behave.runner.DjangoBehaveTestSuiteRunner'
else:
    testing = False

    # From this point forward, all new tables should use the INNODB storage engine.  Setting this will guarantee that
    # any new tables made through Django (sync or migration) will be created using this storage engine. This helps
    # transition the project to using INNODB. If there are every any FK clashes between old MyISAM and new INNODB
    # tables, a South schema migration will be needed to transition the old table to INNODB.
    DATABASES["default"]["STORAGE_ENGINE"] = "INNODB"
