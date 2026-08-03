import os
import re
from urllib.parse import urlsplit

from playwright.sync_api import Page
from pytest_bdd import then, when
from pytest_bdd.parsers import parse

from django.utils.text import slugify

from library.testing.data_compare.pdf import pdf_diff
from library.tests.behavior.steps.page import TOP_DIR


@when(parse('the user checks "{label}"'))
def check(page: Page, label: str):
    page.locator(f'input[name="{label.lower()}"]').check()


@when(parse('the user chooses template type "{template_type}"'))
def choose_template_type(page: Page, template_type: str):
    page.select_option('#id_template_type-template_type', template_type.lower())


@when(parse('the user chooses the existing "{section}" item "{name}"'))
def choose_existing_item(page: Page, section: str, name: str):
    from finances.models import AccountTemplate, BillTemplate, IncomeTemplate

    template = {'account': AccountTemplate, 'bill': BillTemplate, 'income': IncomeTemplate}[section]
    template_id = template.objects.get(name=name).id

    page.locator(f'span.popr[data-id="{section}"]').click()
    page.locator(f'div.popr-item[data-pk="{template_id}"][data-type="{section}"]').first.click()


@when(parse('the user creates a new "{section}" item'))
def create(page: Page, section: str):
    if section not in ['account', 'bill', 'income']:
        assert False, f'create: unknown section ({section})'

    page.locator(f'span.popr[data-id="{section}"]').click()
    page.locator(f'div.popr-item[data-pk=""][data-type="{section}"]').first.click()


@when(parse('the user deletes "{label}"'))
def delete_item(page: Page, label: str):
    page.get_by_role('button', name=label, exact=True).locator('xpath=following-sibling::img').click()


@when(parse('the user hovers over the year "{year}" and selects the statement for "{statement_date}"'))
def hover(page: Page, year: str, statement_date: str):
    page.locator(f'#menu a:text-is("{year}")').hover()
    page.wait_for_timeout(500)
    page.locator(f'#menu a:text-is("{statement_date}")').click()


@when(parse('the user selects {template_type} template "{name}"'))
def select_template(page: Page, template_type: str, name: str):
    page.locator(f'#{template_type.lower()}-button').click()
    page.locator(f'#{template_type.lower()}-menu li', has_text=name).first.click()


@when(parse('the user selects option "{option}"'))
def select_option(page: Page, option: str):
    if page.locator('#id_options').count():
        select = page.locator('#id_options')
    else:
        template_type = page.locator('#id_template_type-template_type').input_value()
        select = page.locator(f'#id_{template_type}-options')

    option_value = select.locator('option', has_text=option).first.get_attribute('value')
    select.select_option(option_value)


@when(parse('the user selects Payment method "{option}"'))
def select_payment_method(page: Page, option: str):
    page.select_option('#popup_id_form-0-payment_method', label=option)


@when(parse('the user selects statement "{name}"'))
def select_statement(page: Page, name: str):
    page.locator('#statement_list-button').click()
    page.locator('#statement_list-menu li', has_text=name).first.click()


@when(parse('the user selects the "{section}" bill "{label}"'))
def select_bill(page: Page, section: str, label: str):
    section = section.lower()
    value = page.locator(f'#{section} option', has_text=label).first.get_attribute('value')
    # Clicking via Playwright doesn't trigger the click event, so we click via JavaScript
    page.evaluate(f'$(".{section}[value=\'{value}\']").click();')


@when(parse('the user sets the "{item}" to "{value}"'))
def set_value(page: Page, item: str, value: str):
    field = 'amount_0' if item == 'Amount' else item.lower().replace(' ', '_')

    if page.locator('h1:text-is("Update Template")').count():
        page.fill(f'#id_{field}', value)
        return

    template_type = page.locator('#id_template_type-template_type')
    if template_type.count():
        page.fill(f'#id_{template_type.input_value()}-{field}', value)
        return

    label = page.locator('form.jqiform:visible label', has_text=f'{item}:').last
    label_for = label.get_attribute('for')
    if label_for:
        page.fill(f'#{label_for}', value)
    else:
        # MoneyField rows render a bare <th> label with the number input in the same row
        label.locator('xpath=ancestor::tr//input').last.fill(value)


@when('the user downloads the PDF version of the statement')
def download_pdf(page: Page, tmp_path):
    from urllib.parse import urljoin

    pdf_path = re.sub(r'^/finances/statement/detail/', '/finances/statement/pdf/', urlsplit(page.url).path) + '/'

    response = page.request.get(urljoin(page.url, pdf_path))
    assert response.status == 200, f'PDF download failed with status {response.status}'
    filename = re.search(r'filename="?([^";]+)"?', response.headers['content-disposition']).group(1)
    assert filename == '2019-12-15.pdf', f'unexpected PDF filename {filename!r}'
    with open(tmp_path / 'statement.pdf', 'wb') as pdf_file:
        pdf_file.write(response.body())


@then('the confirmation number is verified to be correct')
def verify_confirmation_number():
    from datetime import date

    from finances.models import Statement

    assert Statement.objects.get(date=date(2019, 12, 15)).bill_set.get(name='old bill 1').confirmation_number == 'abc123'


@then('the PDF file is verified to be correct')
def verify_pdf(request, tmp_path, snapshot_state, check_images, wip_mode):
    scenario = request.node.__scenario_report__.scenario
    feature = scenario.feature
    app = 'finances' if '/apps/finances/' in feature.filename.replace('\\', '/') else 'library'
    master_image_dir = os.path.join(TOP_DIR, 'tests', app, slugify(feature.name.lower()))

    base_filename = f'{slugify(scenario.name)}-{snapshot_state["pdf_file"]:0>2}.pdf'
    expected_pdf_file = os.path.join(master_image_dir, base_filename)

    if check_images:
        assert os.path.isfile(expected_pdf_file), f'can not find "{expected_pdf_file}" for comparison to PDF file'

        pdf_diff(expected_pdf_file, str(tmp_path / 'statement.pdf'), save2_if_err=base_filename, interactive=wip_mode)

    snapshot_state['pdf_file'] += 1
