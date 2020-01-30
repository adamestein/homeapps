from datetime import datetime

# noinspection PyPackageRequirements
from behave import when


@when('the user downloads the PDF version of the statement')
def download_pdf(context):
    context.browser.find_by_id('pdf').click()
    context.pdf_filename = datetime.strptime(
        context.browser.find_by_tag('h1').first.text,
        'Statement for %B %d, %Y'
    ).strftime('%Y-%m-%d.pdf')
