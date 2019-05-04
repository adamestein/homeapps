from datetime import date
from urlparse import urlsplit

from django.contrib.auth.models import User
from django.core.validators import validate_comma_separated_integer_list
from django.db import models
from django.urls import reverse
from django.utils.dateformat import DateFormat

from djmoney.models.fields import MoneyField

from finances.manager import OptionManager

from library.abstract_models import Auth, StatementItem, Template
from library.ordinal import ordinal


class Account(StatementItem, models.Model):
    account_number = models.CharField(
        blank=True, db_index=True, default='', help_text='Account number.', max_length=30
    )

    class Meta:
        ordering = ('name', 'statement__date')

    @classmethod
    def str_format(cls, name, account_number, amount, item_date=None):
        acct_num = ' (acct #{})'.format(account_number) if account_number else ''
        date_val = ' as of {}'.format(DateFormat(item_date).format('F jS, Y')) if item_date else ''
        return u'{}{} with {}{}'.format(name, acct_num, amount, date_val)

    def __unicode__(self):
        return Account.str_format(self.name, self.account_number, self.amount, self.statement.date)


class AccountTemplate(Template):
    account_number = models.CharField(
        blank=True, db_index=True, default='', help_text='Account number.', max_length=30
    )


class Bill(StatementItem, models.Model):
    PAYMENT_METHOD_CHECK = 0
    PAYMENT_METHOD_DISCOVER = 1
    PAYMENT_METHOD_MASTERCARD = 2
    PAYMENT_METHOD_VISA = 3
    PAYMENT_METHOD_ACCOUNT_TRANSFER = 4
    PAYMENT_METHOD_ACH_DIRECT_DEBIT = 5

    PAYMENT_METHODS = (
        (PAYMENT_METHOD_ACCOUNT_TRANSFER, 'Account Transfer'),
        (PAYMENT_METHOD_ACH_DIRECT_DEBIT, 'ACH - Direct Debit'),
        (PAYMENT_METHOD_CHECK, 'Check'),
        (PAYMENT_METHOD_DISCOVER, 'Credit Card: Discover'),
        (PAYMENT_METHOD_MASTERCARD, 'Credit Card: Mastercard'),
        (PAYMENT_METHOD_VISA, 'Credit Card: VISA'),
    )

    STATE_UNFUNDED = 0
    STATE_UNPAID = 1
    STATE_PAID = 2

    STATES = (
        (STATE_UNFUNDED, 'Unfunded'),
        (STATE_UNPAID, 'Unpaid'),
        (STATE_PAID, 'Paid')
    )

    account_number = models.CharField(
        blank=True, db_index=True, default='', help_text='Account number.', max_length=30
    )
    actual = MoneyField(
        max_digits=10, decimal_places=2, default_currency='USD', blank=True, null=True, help_text='Actual amount paid.'
    )
    check_number = models.PositiveIntegerField(blank=True, null=True, help_text='Check number if paid by check')
    date = models.DateField(db_index=True, help_text='Due date.')
    paid_date = models.DateField(blank=True, null=True, help_text='The date the bill was paid')
    payment_method = models.PositiveSmallIntegerField(choices=PAYMENT_METHODS, null=True, help_text='How bill was paid')
    state = models.PositiveSmallIntegerField(choices=STATES, default=STATE_UNFUNDED, help_text='State of the bill')
    total = MoneyField(
        max_digits=10, decimal_places=2, default_currency='USD', blank=True, null=True,
        help_text="Total amount of the bill if 'amount' is partial."
    )
    options = models.ManyToManyField(
        'Option', help_text='Options for the income.', blank=True, limit_choices_to={'template_type': 'bill'}
    )
    url = models.URLField(blank=True, null=True, help_text='Web site URL used to pay this bill.')

    class Meta:
        ordering = ('name',)

    @property
    def create_display(self):
        total = ' (total is {})'.format(self.total) if self.total else ''

        fstr = '{} for {}{} due on {}'.format(self.name, self.amount, total, DateFormat(self.date).format('F jS, Y'))

        if self.paid_date:
            fstr += ' and paid on ' + DateFormat(self.paid_date).format('F jS, Y')
            fstr += ' ({})'.format(self.actual) if self.actual else ' (PIF)'

        return unicode(fstr)

    @property
    def get_amount(self):
        return self.actual if self.state == Bill.STATE_PAID else self.amount

    @property
    def has_auto_pay(self):
        return self._has_option('Auto Pay')

    @property
    def has_auto_transfer(self):
        return self._has_option('Auto Transfer')

    @property
    def in_paid_state(self):
        return self.state == Bill.STATE_PAID

    @property
    def tracker_display(self):
        return u'{} for {} due on {}'.format(self.name, self.amount, DateFormat(self.date).format('F jS, Y'))

    @property
    def tracker_display_paid(self):
        amount_paid = self.actual if self.actual else self.amount
        return u'{} paid {} on {}'.format(self.name, amount_paid, DateFormat(self.paid_date).format('F jS, Y'))

    def _has_option(self, name):
        option = Option.objects.get(template_type='bill', name=name)
        return option in self.options.all()

    def __unicode__(self):
        state = 'unfunded' if (self.state == self.STATE_UNFUNDED) else 'unpaid' \
            if (self.state == self.STATE_UNPAID) else 'paid'
        total = ' (total is {})'.format(self.total) if self.total else ''

        fstr = '[{}] {} for {}{} due on {}'.format(
            state, self.name, self.amount, total, DateFormat(self.date).format('F jS, Y')
        )

        if self.paid_date:
            fstr += ' and paid on ' + DateFormat(self.paid_date).format('F jS, Y')
            fstr += ' ({})'.format(self.actual) if self.actual else ' (PIF)'

        return unicode(fstr)


class BillTemplate(Template):
    account_number = models.CharField(
        blank=True, db_index=True, default='', help_text='Account number.', max_length=30
    )
    amount = MoneyField(
        max_digits=10, decimal_places=2, default_currency='USD', blank=True, null=True, help_text='Amount of the bill.'
    )
    due_day = models.PositiveSmallIntegerField(
        blank=True, null=True, help_text='Day of the month this bill is due (0 means last day of the month).'
    )
    options = models.ManyToManyField(
        'Option', help_text='Options for the bill.', blank=True, limit_choices_to={'template_type': 'bill'}
    )
    snap_section = models.PositiveSmallIntegerField(help_text='Snap section in which this template should be shown')
    url = models.URLField(blank=True, null=True, help_text='Web site URL used to pay this bill.')

    @property
    def short_url(self):
        parts = urlsplit(self.url)
        url = '{}://{}/'.format(parts.scheme, parts.netloc)
        if len(self.url) > len(url):
            url += '...'
        return unicode(url)

    def __unicode__(self):
        fstr = self.name

        if self.amount:
            fstr += ' for {}'.format(self.amount)

        if self.due_day:
            fstr += ' due on the {} of the month'.format(DateFormat(date(1, 1, self.due_day)).format('jS'))

        return unicode(fstr)


class Income(StatementItem, models.Model):
    account_number = models.CharField(
        blank=True, db_index=True, default='', help_text='Account number.', max_length=30
    )
    date = models.DateField(db_index=True, help_text="Transaction date (date it was deposited).",)
    options = models.ManyToManyField(
        'Option', help_text='Options for the income.', blank=True, limit_choices_to={'template_type': 'income'}
    )

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        fstr = '{} for {} deposited on {}'.format(self.name, self.amount, DateFormat(self.date).format('F jS, Y'))
        if self.account_number:
            fstr += ' into account #{}'.format(self.account_number)
        return unicode(fstr)


class IncomeTemplate(Template):
    account_number = models.CharField(
        blank=True, db_index=True, default='', help_text='Account number.', max_length=30
    )
    amount = MoneyField(
        max_digits=10, decimal_places=2, default_currency='USD', blank=True, null=True, help_text='Income amount.'
    )
    arrival_day = models.PositiveSmallIntegerField(
        blank=True, null=True,
        help_text='Day of the month this income is expected to arrive (0 means last day of the month).'
    )
    options = models.ManyToManyField(
        'Option', help_text='Options for the income.', blank=True, limit_choices_to={'template_type': 'income'}
    )
    snap_section = models.PositiveSmallIntegerField(help_text='Snap section in which this template should be shown')


class Option(models.Model):
    from .template_views import TEMPLATE_CHOICES

    template_type = models.CharField(max_length=7, choices=TEMPLATE_CHOICES[1:])    # Don't include 'account'
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

    objects = OptionManager()

    @property
    def short_label(self):
        return u'{} - {}'.format(self.name, self.description)

    def __unicode__(self):
        return u'{}: {} - {}'.format(self.template_type, self.name, self.description)


class Preference(models.Model):
    user = models.OneToOneField(User)
    snap_days = models.CharField(max_length=5, validators=[validate_comma_separated_integer_list])

    def __unicode__(self):
        days = [int(day) for day in self.snap_days.split(',')]

        if len(days) == 1:
            return u'Snap day set to the {} of the month'.format(ordinal(days[0]))
        else:
            text = 'Snap days set to the '

            if len(days) == 2:
                text += '{} and {}'.format(ordinal(days[0]), ordinal(days[1]))
            else:
                for index, day in enumerate(days):
                    if index == len(days) - 1:
                        text += ', and {}'.format(ordinal(int(day)))
                    elif index:
                        text += ', {}'.format(ordinal(int(day)))
                    else:
                        text += '{}'.format(ordinal(int(day)))

            text += ' of the month'
            return unicode(text)


class Statement(Auth, models.Model):
    date = models.DateField(db_index=True, help_text='Statement date')

    class Meta:
        ordering = ('date', )
        unique_together = (('user', 'date'), )

    def get_absolute_url(self):
        return reverse('statement_detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return unicode(DateFormat(self.date).format('F jS, Y'))
