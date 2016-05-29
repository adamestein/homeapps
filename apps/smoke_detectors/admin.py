from django.contrib import admin
from .models import BatteryInfo, BatteryChangeEvent, Location, SmokeDetector

admin.site.register(BatteryInfo)
admin.site.register(BatteryChangeEvent)
admin.site.register(Location)
admin.site.register(SmokeDetector)
