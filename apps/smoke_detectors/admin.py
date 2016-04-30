from django.contrib import admin
from models import Battery, Event, Location, SmokeDetector

admin.site.register(Battery)
admin.site.register(Event)
admin.site.register(Location)
admin.site.register(SmokeDetector)
