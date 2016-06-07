from django.contrib import admin
from .models import AccountTemplate, BillTemplate, Option

admin.site.register(AccountTemplate)
admin.site.register(BillTemplate)
admin.site.register(Option)
