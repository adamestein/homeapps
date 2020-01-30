# noinspection PyPackageRequirements
from behave import given, when

from splinter.exceptions import ElementDoesNotExist


@given('the user clicks "{}"')
@when('the user clicks "{}"')
def button_click(context, label):
    try:
        # Try finding an actual link first
        context.browser.click_link_by_text(label)
    except ElementDoesNotExist:
        try:
            # If that fails, try finding a button that has the label as a value
            context.browser.find_by_value(label).first.click()
        except ElementDoesNotExist:
            try:
                # If that fails, try finding a button that has the label as text
                context.browser.find_by_xpath(f'//button[normalize-space(text())="{label}"]').first.click()
            except ElementDoesNotExist:
                # If that fails, try finding a button containing a span that has the label as text
                context.browser.find_by_xpath(f'//button/span[normalize-space(text())="{label}"]').first.click()


@given('the user logs in {state}')
def login(context, state):
    context.browser.fill('username', 'user')
    context.browser.fill('password', 'password' if state == 'correctly' else 'bad_password')
    context.browser.find_by_value('login').first.click()
