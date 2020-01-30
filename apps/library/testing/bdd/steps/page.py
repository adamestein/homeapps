import os.path

# noinspection PyPackageRequirements
from behave import given, then

from django.utils.text import slugify

from ..utils import get_screenshot, get_url

from library.testing.data_compare.image import image_diff


@then('the page is verified to be correct')
def verify_page(context):
    _verify_page(context)


@given('the user goes to the home page')
def home_page(context):
    context.browser.visit(get_url(context, '/'))


def _verify_page(context, crop=None, full_page=True, remove_mouse=True, tolerance=10):
    if context.check_images:
        base_filename = '{}-{:0>2}.png'.format(slugify(context.scenario.name), context.screen_shot)
        expected_image_file = os.path.join(context.top_dir, context.master_image_dir, base_filename)

        assert os.path.isfile(expected_image_file), \
            f'can not find "{expected_image_file}" for comparison to screen shot'

        # The trade-off for getting the full page is that it's slower than just getting a screenshot but will get the
        # entire web page no matter what parts are off the screen

        image_diff(
            expected_image_file,
            get_screenshot(context, full_page=full_page, remove_mouse=remove_mouse),
            crop2=crop,
            save2_if_err=base_filename,
            tolerance=tolerance
        )

    context.screen_shot += 1
