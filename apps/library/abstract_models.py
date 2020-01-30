from django.contrib.auth.models import User
from django.db import models

from djmoney.models.fields import MoneyField

from library.middleware.save_requests import get_user


class Auth(models.Model):
    user = models.ForeignKey(User, help_text='To which user this item belongs.')

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not getattr(self, 'user', None):
            # Before we can save the instance, we need to fill in the user field so that we know who the instance belongs to
            self.user = get_user()
        super(Auth, self).save(*args, **kwargs)


class Base(models.Model):
    name = models.CharField(max_length=100, db_index=True, help_text='Name assigned to this item.')

    class Meta:
        abstract = True


class StatementItem(Auth, Base, models.Model):
    amount = MoneyField(
        max_digits=10, decimal_places=2, default_currency='USD', help_text='Current amount in this account.'
    )
    statement = models.ForeignKey('finances.Statement', help_text = 'To which statement this belongs.')

    class Meta:
        abstract = True

    @property
    def model_name(self):
        return self._meta.model_name


class Template(Auth, Base, models.Model):
    disabled = models.BooleanField(default=False, help_text='Check if this template is not to be used.')

    class Meta:
        abstract = True
        ordering = ('name', )
        unique_together = ("name", "user")

    def __str__(self):
        return str(self.name)
