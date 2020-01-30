from datetime import date, datetime
import logging
import re

# noinspection PyPackageRequirements
from forbiddenfruit import curse

# Needed when access is needed to JavaScript console messages
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from splinter.browser import Browser

from django.conf import settings
from django.shortcuts import resolve_url

from .setup import setup
from .utils import get_url


def after_all(context):
    if context.failed and context.config.wip:
        input('Press Enter to quit the browser ...')

    try:
        context.browser.quit()
    except AttributeError:
        # Could get an Attribute error if before_all() exits before a context.browser is created, so we can ignore it
        pass
    else:
        context.browser = None


# noinspection PyUnusedLocal
def after_feature(context, feature):
    # Log out after feature is done so the next feature will have to log in.  No need to log out if there was a
    # failure AND the 'stop' flag is used.  In that case, we want to leave the browser up at the point where the
    # failure was.
    if not context.failed or not context.config.stop:
        context.browser.visit(get_url(context, resolve_url('logout')))


# noinspection PyUnusedLocal
def after_scenario(context, scenario):
    # Need to log out after each scenario is done so that the next scenario can start at the login screen. We
    # could always end each scenario with a step to log out, but then that has to be remembered to be done for
    # each scenario. Easier to do it here. Don't logout if there was an error so that we leave the browser as-is
    # for debugging.
    if not context.failed or not context.config.stop:
        context.browser.visit(get_url(context, resolve_url('logout')))


def after_tag(context, tag):
    if tag == "pause":
        context.pause = False


def before_all(context):
    context.check_images = context.config.userdata.get('check_images',  'True') == 'True'

    # Temp directory for any downloaded files
    from tempfile import TemporaryDirectory
    context.tmp_dir = TemporaryDirectory(dir='/tmp')

    # In case logging is not captured
    if not context.config.log_capture:
        logging.basicConfig(level=logging.DEBUG)

    # Default to Chrome if not set
    browser = "chrome" if not context.config.browser else context.config.browser

    if browser == 'chrome':
        from selenium.webdriver.chrome.options import Options

        options = Options()

        # Turn off Chrome asking to save the password and strict W3C mode
        options.add_experimental_option(
            'prefs',
            {
                'credentials_enable_service': False,
                'download.default_directory': context.tmp_dir.name,
                'profile': {'password_manager_enabled': False},
                'w3c': False
            }
        )

        # Uncomment the following lines if JavaScript console messages need to be examined
        # d = DesiredCapabilities.CHROME
        # d['loggingPrefs'] = {'browser': 'ALL'}
        # context.browser = Browser(browser, options=options, desired_capabilities=d)

        context.browser = Browser(browser, options=options)
    else:
        context.browser = Browser(browser)

    # Lock in the date and time to avoid anything that uses a relative datetime value. We don't have to worry
    # about restoring the original functions as all behavior tests will use the set datetime value.
    curse(date, 'today', classmethod(lambda cls: date(2020, 1, 8)))
    curse(datetime, 'now', classmethod(lambda cls, tz=None: datetime(2020, 1, 8)))
    curse(datetime, 'today', classmethod(lambda cls: datetime(2020, 1, 8)))

    # Save the top directory location, used to find files
    context.top_dir = re.sub('apps/library/testing/bdd/environment.pyc?', '', __file__)

    settings.DEBUG = True
    settings.VERSION = '<version>'      # So that we don't have to update master images ever time version changes

    # Set up the database
    setup()


# noinspection PyUnusedLocal
def before_step(context, step):
    # Store the step number if needed (starts at 1)
    if 'step_number' not in context:
        context.step_number = 0
    context.step_number += 1

    if "pause" in context and context.pause:
        input('Press Enter to execute this step ...')


def before_tag(context, tag):
    if tag == "pause":
        context.pause = True
