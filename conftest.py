import datetime
import os
from pathlib import Path
import re
import sys

# Playwright's sync API runs its asyncio loop in a paused greenlet and, after every page call, sets
# asyncio's "_running_loop" ContextVar in the test's contextvars context. Django's @async_unsafe guard then
# mistakes the main thread for an async context and raises SynchronousOnlyOperation (e.g. when the
# TransactionTestCase teardown calls check_constraints), so disable that guard for the whole pytest process.
os.environ.setdefault('DJANGO_ALLOW_ASYNC_UNSAFE', '1')

from forbiddenfruit import curse
import pytest

from django.conf import settings

from library.tests.behavior.steps.common import pause

# The apps directory holds all the importable packages and is only put on sys.path when the Django
# settings module is imported, which happens after conftests load. Add it here so the pytest_plugins
# below can be imported.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'apps')))

pytest_plugins = [
    'library.tests.behavior.steps.common',
    'library.tests.behavior.steps.form',
    'library.tests.behavior.steps.page',
]


def pytest_addoption(parser):
    parser.addoption(
        '--no-images',
        action='store_true',
        default=False,
        help='Skip golden image comparisons in behavior tests'
    )


def _trace_print(request, text):
    # The wip trace must be visible live (so you can see which step is running), but pytest captures
    # stdout/stderr during test execution. Suspend that capture around the print, then resume it.
    capman = request.config.pluginmanager.getplugin('capturemanager')
    if capman is not None:
        capman.suspend_global_capture()
    try:
        print(text, flush=True)
    finally:
        if capman is not None:
            capman.resume_global_capture()


def _wip_run(request):
    # Match the wip keyword as a positive selector only, so -m "not wip" doesn't enable tracing.
    return bool(re.search(r'(?<!not\s)\bwip\b', request.config.getoption('-m') or ''))


@pytest.hookimpl(tryfirst=True)
def pytest_bdd_before_scenario(request, feature, scenario):
    # Stash the scenario's starting line so pytest_runtest_makereport can splice it into
    # rep.nodeid for the short test summary, regardless of how the scenario later fails.
    request.node._bdd_scenario_line = scenario.line_number
    request.node._bdd_feature_path = _get_relative_path(Path(feature.filename))

    if not _wip_run(request):
        return

    relative_path = _get_relative_path(Path(feature.filename))
    seen_features = getattr(request.session, "_seen_features", set())

    if feature.filename not in seen_features:
        seen_features.add(feature.filename)
        request.session._seen_features = seen_features
        _trace_print(request, f'\n\nFeature: {feature.name} # .../{relative_path}:{feature.line_number}\n')
    else:
        _trace_print(request, '\n')

    # Print tags if present
    if scenario.tags:
        _trace_print(request, f"  {' '.join(['@' + tag for tag in scenario.tags])}")

    # Subtract to line things up given placement of scenario name, step keyword and name
    request.config.step_name_width = max([len(f'{step.keyword} {step.name}') for step in scenario.steps])

    _trace_print(
        request,
        f'  Scenario: {scenario.name:<{request.config.step_name_width-8}} # .../{relative_path}:{scenario.line_number}'
    )

    # Reset step by step for this scenario
    request.config.stepbystep = False


def pytest_bdd_before_step(request, step, step_func):
    if not _wip_run(request):
        return

    relative_path = _get_relative_path(Path(step_func.__code__.co_filename))
    step_name = f'{step.keyword} {step.name}'

    _trace_print(
        request,
        f'    {step_name:<{request.config.step_name_width}} # .../{relative_path}:{step_func.__code__.co_firstlineno}'
        f' (test line {step.line_number})'
    )

    if request.config.stepbystep:
        pause(request)


def pytest_configure(config):
    config.browser_desktop = os.getenv('BDD_BROWSER_DESKTOP')


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    line = getattr(item, '_bdd_scenario_line', None)
    feature_path = getattr(item, '_bdd_feature_path', None)
    if rep.failed and line and feature_path:
        # nodeid is "<path>.py::test_name"; replace the .py path with the .feature path and splice
        # ":NN" so the FAILED summary line reads "statements.feature:136::test_view_previous_statements"
        # — always visible and lets you jump straight to the failing scenario in the .feature file
        # (NN is that scenario's first line there). The nodeid is never width-trimmed in the summary.
        rep.nodeid = f'{feature_path}:{line}::' + rep.nodeid.split('::', 1)[1]


@pytest.fixture
def check_images(pytestconfig):
    return not pytestconfig.getoption('--no-images')


# Interactive comparison (GUI dialog to save a new master and retry) is only useful while developing
# a test, i.e. when selecting the @wip-marked scenarios via `-m wip`. The flag is session-fixed, so
# compute it once from the marker expression rather than per comparison.
@pytest.fixture(scope='session')
def wip_mode(pytestconfig):
    return 'wip' in (pytestconfig.getoption('-m') or '')


# Match the window size the master images were captured with so full-page screenshots stay 1050 px wide
@pytest.fixture
def browser_context_args():
    return {'viewport': {'width': 1050, 'height': 752}}


@pytest.fixture(scope='session')
def browser_type_launch_args(pytestconfig):
    launch_options = {}
    if pytestconfig.getoption('--headed'):
        launch_options['headless'] = False
    browser_channel = pytestconfig.getoption('--browser-channel')
    if browser_channel:
        launch_options['channel'] = browser_channel
    slowmo = pytestconfig.getoption('--slowmo')
    if slowmo:
        launch_options['slow_mo'] = slowmo
    return launch_options


@pytest.fixture(scope='session')
def _freeze_time():
    # Lock in the date and time to avoid anything that uses a relative datetime value. There's no need to
    # restore the original functions as behavior tests are the only ones that use this value.
    curse(datetime.date, 'today', classmethod(lambda cls: datetime.date(2020, 1, 8)))
    curse(datetime.datetime, 'now', classmethod(lambda cls, tz=None: datetime.datetime(2020, 1, 8)))
    curse(datetime.datetime, 'today', classmethod(lambda cls: datetime.datetime(2020, 1, 8)))


# Function-scoped because TransactionTestCase flushes every table after each test, so the session-level
# rows would not survive to the next test.
@pytest.fixture
def seed_base_data(django_db_blocker, django_db_setup):
    from django.contrib.auth.models import User

    from finances.models import Option, Preference

    with django_db_blocker.unblock():
        # LiveServerTestCase doesn't reset row IDs, so we need to be specific
        user = User(id=1, is_staff=True, is_superuser=True, username='user')
        user.set_password('password')
        user.save()

        # The constance config table is flushed with everything else after each test. The app list the
        # templates render from (config.APPS) is normally written by app_autodiscover() when the URLConf is
        # first imported, so without this the second test on would see an empty app list.
        from library.autodiscover import app_autodiscover

        app_autodiscover()

        Preference.objects.create(snap_days='1, 15', user=user)

        options = {
            'bill_option_1': Option.objects.create(
                description='sample bill option 1', name='option 1', template_type='bill'
            ),
            'bill_option_2': Option.objects.create(
                description='sample bill option 2', name='option 2', template_type='bill'
            ),
            'income_option_1': Option.objects.create(
                description='sample income option 1', name='option 1', template_type='income'
            ),
            'income_option_2': Option.objects.create(
                description='sample income option 2', name='option 2', template_type='income'
            ),
        }

        return {'user': user, **options}


@pytest.fixture
def seed_scenario_data(seed_base_data, transactional_db):
    from datetime import date

    from finances.models import AccountTemplate, BillTemplate, IncomeTemplate, Statement

    user = seed_base_data['user']

    AccountTemplate.objects.create(account_number='existing_acct_001', name='Existing Account #1', user=user)
    AccountTemplate.objects.create(account_number='delete_me', name='Delete This Account Template', user=user)

    BillTemplate.objects.create(
        account_number='existing_bill_001', due_day=10, amount='435.33',
        name='Existing Bill #1', snap_section=1, user=user
    )
    BillTemplate.objects.create(
        account_number='delete_me', due_day=1, amount='0',
        name='Delete This Bill Template', snap_section=2, user=user
    )

    IncomeTemplate.objects.create(
        account_number='existing_income_001', amount=1045,
        name='Existing Income #1', snap_section=1, user=user
    )
    IncomeTemplate.objects.create(
        account_number='delete_me', amount=0,
        name='Delete This Income Template', snap_section=2, user=user
    )

    statement = Statement.objects.create(date=date(2019, 12, 15), user=user)

    statement.account_set.create(account_number='old acct #1', amount='0.03', name='old account 1', user=user)
    statement.account_set.create(account_number='old acct #2', amount='445.98', name='old account 2', user=user)

    statement.bill_set.create(
        account_number='old bill #1', amount='34.45', date=date(2019, 12, 28),
        name='old bill 1', total='100', user=user
    )

    bill_2 = statement.bill_set.create(
        amount='40', date=date(2019, 12, 20), name='old bill 2', user=user,
        url='http://www.payyerbillhere.com/'
    )
    bill_2.options.add(seed_base_data['bill_option_1'])
    bill_2.options.add(seed_base_data['bill_option_2'])

    statement.income_set.create(
        account_number='old income #1', amount='4539.34', date=date(2019, 12, 16),
        name='old income 1', user=user
    )

    income_2 = statement.income_set.create(amount='450', date=date(2019, 12, 17), name='old income 2', user=user)
    income_2.options.add(seed_base_data['income_option_1'])
    income_2.options.add(seed_base_data['income_option_1'])

    return {'statement': statement}


@pytest.fixture
def snapshot_state():
    return {'screen_shot': 1, 'pdf_file': 1}


@pytest.fixture(autouse=True)
def _behavior_environment(request):
    if not request.node.get_closest_marker('behavior'):
        yield
        return

    # The live server runs in another thread, so tests must be marked django_db(transaction=True) for its
    # connection to see the seeded rows (a non-transactional TestCase wraps the test in an uncommitted
    # transaction, and the orphaned connection would also hold SQLite write locks at teardown).
    request.getfixturevalue('_freeze_time')
    request.getfixturevalue('seed_base_data')
    request.getfixturevalue('seed_scenario_data')

    live_server = request.getfixturevalue('live_server')

    from urllib.parse import urlsplit
    host = urlsplit(live_server.url).hostname
    original_allowed_hosts = settings.ALLOWED_HOSTS
    settings.ALLOWED_HOSTS = [*original_allowed_hosts, host]

    # Pin the version the footer renders so master images don't go stale when VERSION in
    # settings/base.py is bumped on user-visible changes.
    original_version = settings.VERSION
    settings.VERSION = '<version>'

    yield

    settings.VERSION = original_version
    settings.ALLOWED_HOSTS = original_allowed_hosts


def _get_relative_path(file_path):
    # Get relative path from current working directory
    file_path = Path(file_path).resolve()
    try:
        return file_path.relative_to(Path.cwd())
    except ValueError:
        # If file is not inside the project root, return as-is
        return file_path
