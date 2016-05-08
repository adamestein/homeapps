from django.contrib import admin
from models import BatteryInfo, Event, Location, SmokeDetector

admin.site.register(BatteryInfo)
admin.site.register(Event)
admin.site.register(Location)
admin.site.register(SmokeDetector)
