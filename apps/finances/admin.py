from django.contrib import admin
from .models import AccountTemplate, BillTemplate, IncomeTemplate, Option

admin.site.register(AccountTemplate)
admin.site.register(BillTemplate)
admin.site.register(IncomeTemplate)
admin.site.register(Option)
