from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Account, AccountTemplate, Bill, BillTemplate, Income, IncomeTemplate, Option, Preference, Statement


# Define an inline admin descriptor for the Preference model which acts a bit like a singleton
class PreferenceInline(admin.StackedInline):
    model = Preference
    can_delete = False


# Define a new User admin
class UpdatedUserAdmin(UserAdmin):
    inlines = (PreferenceInline, )

admin.site.register(Account)
admin.site.register(AccountTemplate)
admin.site.register(Bill)
admin.site.register(BillTemplate)
admin.site.register(Income)
admin.site.register(IncomeTemplate)
admin.site.register(Option)
admin.site.register(Statement)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UpdatedUserAdmin)
