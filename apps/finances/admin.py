from django.contrib import admin
from .models import Account, AccountTemplate, BillTemplate, IncomeTemplate, Option, Statement

admin.site.register(Account)
admin.site.register(AccountTemplate)
admin.site.register(BillTemplate)
admin.site.register(IncomeTemplate)
admin.site.register(Option)
admin.site.register(Statement)
