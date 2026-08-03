from playwright.sync_api import Page
from pytest_bdd import given, when
from pytest_bdd.parsers import parse


@given(parse('the user clicks "{label}"'))
@when(parse('the user clicks "{label}"'))
def button_click(page: Page, label: str):
    page.wait_for_load_state('load')
    locator = page.get_by_role('link', name=label, exact=True)
    if locator.count():
        locator.first.click()
        return

    locator = page.locator(f'input[value="{label}"]')
    if locator.count():
        locator.first.click()
        return

    locator = page.locator(f'div.popr-item:visible:text-is("{label}")')
    if locator.count():
        locator.first.click()
        return

    page.get_by_role('button', name=label, exact=True).click()


@given(parse('the user logs in {state}'))
def login(page: Page, state: str):
    page.fill('input[name="username"]', 'user')
    page.fill('input[name="password"]', 'password' if state == 'correctly' else 'bad_password')
    page.locator('input[value="login"]').click()
