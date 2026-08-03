import os
import re
from urllib.parse import urlsplit

from playwright.sync_api import Page
from pytest_bdd import given, then

from django.utils.text import slugify

from library.testing.data_compare.image import image_diff

TOP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))


@given('the user goes to the home page')
def home_page(live_server, page: Page):
    page.goto(live_server.url + '/')


@then('the page is verified to be correct')
def verify_page(check_images, page: Page, request, snapshot_state, wip_mode):
    _verify_page(page, request, check_images, snapshot_state, wip_mode)


def _verify_page(page, request, check_images, snapshot_state, wip_mode):
    header = page.locator('h1').inner_text()
    expected = expected_header(urlsplit(page.url).path)
    if isinstance(expected, tuple):
        expected, exact = expected
    else:
        exact = True

    if exact:
        assert header == expected, f'expected header "{expected}" but got "{header}" at {page.url}'
    else:
        assert header.startswith(expected), f'expected header starting with "{expected}" but got "{header}" at {page.url}'

    if check_images:
        scenario = request.node.__scenario_report__.scenario
        feature = scenario.feature
        app = 'finances' if '/apps/finances/' in feature.filename.replace('\\', '/') else 'library'
        master_image_dir = os.path.join(TOP_DIR, 'tests', app, slugify(feature.name.lower()))

        base_filename = f'{slugify(scenario.name)}-{snapshot_state["screen_shot"]:0>2}.png'
        expected_image_file = os.path.join(master_image_dir, base_filename)

        assert os.path.isfile(expected_image_file), \
            f'can not find "{expected_image_file}" for comparison to screen shot'

        image_diff(
            expected_image_file,
            get_screenshot(page),
            save2_if_err=base_filename,
            tolerance=10,
            interactive=wip_mode
        )

    snapshot_state['screen_shot'] += 1


def get_screenshot(page, full_page=True, remove_caret=True, remove_mouse=True):
    if remove_mouse:
        # Move the mouse to a corner so a link that was just clicked isn't left in its :hover state,
        # which would give it a different background color in the screen shot than the other boxes.
        page.mouse.move(0, 0)

    if remove_caret:
        # Make the focused input's caret invisible so it can't show up in the screen shot
        page.evaluate(
            '''
            if (window.jQuery) {
                var focused = $(document).find(":focus");
                if (focused.length && focused.prop("tagName") === "INPUT") {
                    focused.css("color", "transparent").css("text-shadow", "0 0 0 #000");
                }
            }
            '''
        )
        page.wait_for_timeout(500)

    screenshot = page.screenshot(full_page=full_page)

    if remove_caret:
        # Restore caret color back to normal
        page.evaluate(
            '''
            if (window.jQuery) {
                var focused = $(document).find(":focus");
                if (focused.length && focused.prop("tagName") === "INPUT") {
                    focused.css("color", "rgb(0, 0, 0)").css("text-shadow", "");
                }
            }
            '''
        )

    return screenshot


def expected_header(path):
    """Map a URL path to the '<h1>' text the page should show (or a prefix if the page is date-dependent)."""
    if path == '/':
        return 'Home Applications'
    if path == '/accounts/login/':
        return 'Home Apps Login'
    if path == '/finances/':
        return 'Financial Applications'
    if path == '/utilities/':
        return 'Utility Applications'
    if path.startswith('/finances/statement/create/'):
        return 'Create Statement'
    if path.startswith('/finances/statement/detail/'):
        return ('Statement for', False)
    if re.match(r'^/finances/statement/edit/\d+', path):
        return 'Update Statement'
    if path.startswith('/finances/statement/edit/') or path.startswith('/finances/statement/list/'):
        return 'Finances: Statement List'
    if path.startswith('/finances/template/create/'):
        return 'Create Template'
    if re.match(r'^/finances/template/edit/[a-z]+/\d+', path):
        return 'Update Template'
    if path.startswith('/finances/template/edit/'):
        return 'Edit Template'
    if path.startswith('/finances/template/list/'):
        return 'List Templates'
    if path.startswith('/finances/tracker/list/'):
        return 'Finances: Trackable Statements'
    if re.match(r'^/finances/tracker/\d+', path):
        return 'Finances: Bill Payment Tracker'
    raise AssertionError(f'no expected header mapping for path {path!r}')
