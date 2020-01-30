import os

# noinspection PyPackageRequirements
from behave import then

from django.utils.text import slugify

from library.testing.data_compare.pdf import pdf_diff


@then('the PDF file is verified to be correct')
def verify_pdf(context):
    base_filename = '{}-{:0>2}.pdf'.format(slugify(context.scenario.name), context.pdf_file)
    expected_pdf_file = os.path.join(context.top_dir, context.master_image_dir, base_filename)

    assert os.path.isfile(expected_pdf_file), f'can not find "{expected_pdf_file}" for comparison to PDF file'

    pdf_diff(expected_pdf_file, os.path.join(context.tmp_dir.name, context.pdf_filename), save2_if_err=base_filename)

    context.pdf_file += 1
