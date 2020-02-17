from time import sleep

# noinspection PyPackageRequirements
from behave import when
from selenium.webdriver.common.action_chains import ActionChains

from finances.models import AccountTemplate, BillTemplate, IncomeTemplate


@when('the user checks "{label}"')
def check(context, label):
    context.browser.check(label.lower())


@when('the user chooses template type "{template_type}"')
def choose_template_type(context, template_type):
    context.browser.select('template_type-template_type', template_type.lower())


@when('the user chooses the existing "{section}" item "{name}"')
def choose_existing_item(context, section, name):
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


@when('the user selects {template_type} template "{name}"')
def select_template(context, template_type, name):
    context.browser.find_by_id(f'{template_type.lower()}-button').first.click()
    context.browser.find_by_id(f'{template_type.lower()}-menu').find_by_text(name).first.click()


@when('the user selects option "{option}"')
def select_option(context, option):
    if context.browser.find_by_id('id_options'):
        context.browser.select(
            'options',
            context.browser.find_by_xpath(f'//select/option[normalize-space(text())="{option}"]').value
        )
    else:
        context.browser.select(
            f'{context.browser.find_by_id("id_template_type-template_type").first.value}-options',
            context.browser.find_by_xpath(f'//select/option[normalize-space(text())="{option}"]').value
        )


@when('the user selects Payment method "{option}"')
def select_payment_method(context, option):
    # Can't use the normal Splinter select() function as there are two 'Payment method' widgets with the same name,
    # one visible, one not. That way, the HTML can be copied into the popup when needed. It's this popup version
    # that's visible and the one we want to affect.
    context.browser.find_by_xpath(
        f'//*[@id="popup_id_form-0-payment_method"]/option[normalize-space(text())="{option}"]'
    ).first.click()


@when('the user selects statement "{name}"')
def select_statement(context, name):
    context.browser.find_by_id('statement_list-button').first.click()

    for elem in context.browser.find_by_text(name):
        if elem.tag_name == 'li':
            elem.click()


@when('the user selects the "{section}" bill "{label}"')
def select_bill(context, section, label):
    # Clicking via Splinter doesn't trigger the click event, so we click via JavaScript
    elem = context.browser.find_by_id(section.lower()).find_by_xpath(f'//option[contains(text(), "{label}")]').first
    section = section.lower()
    context.browser.execute_script(f'$(".{section}[value=\'{elem.value}\']").click();')


@when('the user sets the "{item}" to "{value}"')
def set_value(context, item, value):
    if context.browser.find_by_xpath(f'//h1[normalize-space(text())="Update Template"]'):
        if item == 'Amount':
            item = 'amount_0'

        context.browser.find_by_id(f'id_{item.lower().replace(" ", "_")}').first.value = value
    else:
        template_type = context.browser.find_by_id('id_template_type-template_type')
        if template_type:
            if item == 'Amount':
                item = 'amount_0'

            context.browser.find_by_id(
                f'id_{template_type.first.value}-{item.lower().replace(" ", "_")}'
            ).first.value = value
        else:
            # Try finding a visible element 4 times (up to 4 seconds)
            for _ in range(10):
                # Only one form element should be visible, so we just look for the first one that's visible and use that
                for elem in context.browser.find_by_tag('form[class="jqiform "]').find_by_text(f'{item}:'):
                    if elem.visible:
                        context.browser.find_by_id(elem['for']).first.value = value
                        return

                sleep(1)

            assert False, f'set_value: failed to set "{item}" with the value "{value}"'
