from django.contrib import admin
from .models import AccountTemplate, BillTemplate

admin.site.register(AccountTemplate)
admin.site.register(BillTemplate)
