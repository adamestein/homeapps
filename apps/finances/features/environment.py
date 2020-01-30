from datetime import date

from selenium.webdriver.common.action_chains import ActionChains

from django.contrib.auth.models import User
from django.utils.text import slugify

from finances.models import AccountTemplate, BillTemplate, IncomeTemplate, Option, Preference, Statement

# noinspection PyUnresolvedReferences
from library.testing.bdd.environment import (
    after_all, after_feature, after_scenario as super_after_scenario, after_tag, before_all, before_step, before_tag
)


def after_scenario(context, scenario):
    if scenario.name == 'Create Statement':
        Statement.objects.exclude(date=date(2019, 12,15)).delete()

    super_after_scenario(context, scenario)


def before_feature(context, feature):
    # Set up to verify pages by image comparison
    context.master_image_dir = f'{context.top_dir}tests/finances/{slugify(feature.name.lower())}'

    user = User.objects.get(username='user')

    AccountTemplate.objects.create(
        account_number='existing_acct_001',
        name='Existing Account #1',
        user=user
    )

    BillTemplate.objects.create(
        account_number='existing_bill_001',
        due_day=10,
        amount='435.33',
        name='Existing Bill #1',
        snap_section=1,
        user=user
    )

    IncomeTemplate.objects.create(
        account_number='existing_income_001',
        amount=1045,
        name='Existing Income #1',
        snap_section=1,
        user=user
    )

    Preference.objects.create(
        snap_days='1, 15',
        user=user
    )


# noinspection PyUnusedLocal
def before_scenario(context, scenario):
    context.pdf_file = 0        # Used to determine which PDF file to use for verification
    context.screen_shot = 0     # Used to determine which image file to use to verify page looks correct

    # Reset mouse position back to start in case previous scenario left it over a popup menu
    origin = context.browser.driver.find_element_by_xpath('//html')
    ActionChains(context.browser.driver).move_to_element(origin).perform()

    _load_database()


def _load_database():
    Statement.objects.all().delete()

    user = User.objects.get(username='user')

    statement = Statement.objects.create(
        date=date(2019, 12, 15),
        user=user
    )

    statement.account_set.create(
        account_number='old acct #1',
        amount='0.03',
        name='old account 1',
        user=user
    )

    statement.account_set.create(
        account_number='old acct #2',
        amount='445.98',
        name='old account 2',
        user=user
    )

    statement.bill_set.create(
        account_number='old bill #1',
        amount='34.45',
        date=date(2019, 12, 28),
        name='old bill 1',
        total='100',
        user=user
    )

    opt1 = Option.objects.create(
        description='sample bill option 1',
        name='option 1',
        template_type='bill'
    )

    opt2 = Option.objects.create(
        description='sample bill option 2',
        name='option 2',
        template_type='bill'
    )

    bill = statement.bill_set.create(
        amount='40',
        date=date(2019, 12, 20),
        name='old bill 2',
        user=user,
        url='http://www.payyerbillhere.com/'
    )
    bill.options.add(opt1)
    bill.options.add(opt2)

    statement.income_set.create(
        account_number='old income #1',
        amount='4539.34',
        date=date(2019, 12, 16),
        name='old income 1',
        user=user
    )

    opt1 = Option.objects.create(
        description='sample income option 1',
        name='option 1',
        template_type='income'
    )

    opt2 = Option.objects.create(
        description='sample income option 2',
        name='option 2',
        template_type='income'
    )

    income = statement.income_set.create(
        amount='450',
        date=date(2019, 12, 17),
        name='old income 2',
        user=user
    )
    income.options.add(opt1)
    income.options.add(opt2)
