from datetime import date

from selenium.webdriver.common.action_chains import ActionChains

from django.contrib.auth.models import User
from django.utils.text import slugify

from finances.models import AccountTemplate, BillTemplate, IncomeTemplate, Option, Preference, Statement

# noinspection PyUnresolvedReferences
from library.testing.bdd.environment import (
    after_all, after_feature, after_scenario, after_tag, before_all as super_before_all, before_step, before_tag
)


def before_all(context):
    super_before_all(context)

    context.user = User.objects.get(username='user')

    Preference.objects.create(
        snap_days='1, 15',
        user=context.user
    )


def before_feature(context, feature):
    # Set up to verify pages by image comparison
    context.master_image_dir = f'{context.top_dir}tests/finances/{slugify(feature.name.lower())}'

    context.bill_option_1 = Option.objects.create(
        description='sample bill option 1',
        name='option 1',
        template_type='bill'
    )

    context.bill_option_2 = Option.objects.create(
        description='sample bill option 2',
        name='option 2',
        template_type='bill'
    )

    context.income_option_1 = Option.objects.create(
        description='sample income option 1',
        name='option 1',
        template_type='income'
    )

    context.income_option_2 = Option.objects.create(
        description='sample income option 2',
        name='option 2',
        template_type='income'
    )


# noinspection PyUnusedLocal
def before_scenario(context, scenario):
    context.pdf_file = 0        # Used to determine which PDF file to use for verification
    context.screen_shot = 0     # Used to determine which image file to use to verify page looks correct

    # Reset mouse position back to start in case previous scenario left it over a popup menu
    origin = context.browser.driver.find_element_by_xpath('//html')
    ActionChains(context.browser.driver).move_to_element(origin).perform()

    _load_database(context)


def _load_database(context):
    AccountTemplate.objects.all().delete()
    BillTemplate.objects.all().delete()
    IncomeTemplate.objects.all().delete()
    Statement.objects.all().delete()

    AccountTemplate.objects.create(
        account_number='existing_acct_001',
        name='Existing Account #1',
        user=context.user
    )

    AccountTemplate.objects.create(
        account_number='delete_me',
        name='Delete This Account Template',
        user=context.user
    )

    BillTemplate.objects.create(
        account_number='existing_bill_001',
        due_day=10,
        amount='435.33',
        name='Existing Bill #1',
        snap_section=1,
        user=context.user
    )

    BillTemplate.objects.create(
        account_number='delete_me',
        due_day=1,
        amount='0',
        name='Delete This Bill Template',
        snap_section=2,
        user=context.user
    )

    IncomeTemplate.objects.create(
        account_number='existing_income_001',
        amount=1045,
        name='Existing Income #1',
        snap_section=1,
        user=context.user
    )

    IncomeTemplate.objects.create(
        account_number='delete_me',
        amount=0,
        name='Delete This Income Template',
        snap_section=2,
        user=context.user
    )

    statement = Statement.objects.create(
        date=date(2019, 12, 15),
        user=context.user
    )

    statement.account_set.create(
        account_number='old acct #1',
        amount='0.03',
        name='old account 1',
        user=context.user
    )

    statement.account_set.create(
        account_number='old acct #2',
        amount='445.98',
        name='old account 2',
        user=context.user
    )

    statement.bill_set.create(
        account_number='old bill #1',
        amount='34.45',
        date=date(2019, 12, 28),
        name='old bill 1',
        total='100',
        user=context.user
    )

    bill = statement.bill_set.create(
        amount='40',
        date=date(2019, 12, 20),
        name='old bill 2',
        user=context.user,
        url='http://www.payyerbillhere.com/'
    )
    bill.options.add(context.bill_option_1)
    bill.options.add(context.bill_option_2)

    statement.income_set.create(
        account_number='old income #1',
        amount='4539.34',
        date=date(2019, 12, 16),
        name='old income 1',
        user=context.user
    )

    income = statement.income_set.create(
        amount='450',
        date=date(2019, 12, 17),
        name='old income 2',
        user=context.user
    )
    income.options.add(context.income_option_1)
    income.options.add(context.income_option_1)
