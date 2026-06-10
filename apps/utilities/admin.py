from django.contrib import admin

from .models import ElectricGasStatement, WaterStatement


admin.site.register(ElectricGasStatement)
admin.site.register(WaterStatement)
