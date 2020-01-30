from time import sleep

# noinspection PyPackageRequirements
from behave import when
from selenium.webdriver.common.action_chains import ActionChains

from finances.models import AccountTemplate, BillTemplate, IncomeTemplate


@when('the user chooses the existing "{section}" item "{name}"')
def choose_existing(context, section, name):
    if section == 'account':
        template_id = AccountTemplate.objects.get(name=name).id
    elif section == 'bill':
        template_id = BillTemplate.objects.get(name=name).id
    elif section == 'income':
        template_id = IncomeTemplate.objects.get(name=name).id
    else:
        assert False, f'choose_existing: unknown section ({section})'

    context.browser.find_by_tag(f'span[class="popr"][data-id="{section}"]').first.click()
    context.browser.find_by_tag(f'div[class="popr-item"][data-pk="{template_id}"][data-type="{section}"]').first.click()


@when('the user creates a new "{section}" item')
def create(context, section):
    if section not in ['account', 'bill', 'income']:
        assert False, f'create: unknown section ({section})'

    context.browser.find_by_tag(f'span[class="popr"][data-id="{section}"]').first.click()
    context.browser.find_by_tag(f'div[class="popr-item"][data-pk=""][data-type="{section}"]').first.click()


@when('the user deletes "{label}"')
def delete_item(context, label):
    context.browser.find_by_xpath(f'//button[normalize-space(text())="{label}"]/following-sibling::img').first.click()


@when('the user hovers over the year "{year}" and selects the statement for "{statement_date}"')
def hover(context, year, statement_date):
    elem = context.browser.find_link_by_text(year).first._element
    ActionChains(context.browser.driver).move_to_element(elem).perform()
    context.browser.find_link_by_text(statement_date).first.click()


@when('the user sets the "{item}" to "{value}"')
def set_value(context, item, value):
    # Try finding a visible element 4 times (up to 4 seconds)
    for _ in range(10):
        # Only one form element should be visible, so we just look for the first one that's visible and use that
        for elem in context.browser.find_by_tag('form[class="jqiform "]').find_by_text(f'{item}:'):
            if elem.visible:
                context.browser.find_by_id(elem['for']).first.value = value
                return

        sleep(1)

    assert False, f'set_value: failed to set "{item}" with the value "{value}"'
