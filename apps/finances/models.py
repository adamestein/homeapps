from django.db import models

from library.models.abstract import Template

# Leave commented out until we have a Statement model in place
# class AccountSummary(models.Model):
#     account = models.ForeignKey("AccountTemplate", help_text="Account template.")
#     amount = MoneyField(help_text='Current amount in this account.')
#     statement = models.ForeignKey("Statement", help_text = "To which statement this account summary belongs.",)


class AccountTemplate(Template):
    account_number = models.PositiveIntegerField(
        db_index=True, blank=True, null=True, default='', help_text="Account number."
    )
