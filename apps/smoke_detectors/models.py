from datetime import date

from django.db import models


# Battery information
class Battery(models.Model):
    BATTERY_TYPES = (
        ("9v", "9 volt"),
        ("AA", "AA"),
        ("AAA", "AAA"),
        ("C", "C"),
        ("D", "D")
    )

    type = models.CharField(max_length=3, choices=BATTERY_TYPES, help_text='Battery Type')
    number = models.PositiveSmallIntegerField(help_text='Number of batteries required by this smoke detector')

    class Meta:
        verbose_name_plural = 'Batteries'

    def __unicode__(self):
        return u'{} of type {}'.format(self.number, self.type)


# Battery change event
class Event(models.Model):
    detector = models.ForeignKey('SmokeDetector', help_text='Smoke detector this event is for')
    date = models.DateField(default=date.today, db_index=True, help_text='Battery change date')

    class Meta:
        ordering = ['date']

    def __unicode__(self):
        return u'Change battery event on {}'.format(date.strftime(self.date, '%A %B %d, %Y'))


# Smoke detector location
class Location(models.Model):
    location = models.CharField(max_length=50, help_text='Location of detector')

    class Meta:
        ordering = ['location']

    def __unicode__(self):
        return self.location


# Smoke detectors
class SmokeDetector(models.Model):
    location = models.ForeignKey(Location, help_text='Location of the smoke detector')
    battery_type = models.ForeignKey(Battery, help_text='Type of battery the smoke detector uses')

    class Meta:
        ordering = ['location']

    def __unicode__(self):
        return u'Smoke detector at {}'.format(self.location)
