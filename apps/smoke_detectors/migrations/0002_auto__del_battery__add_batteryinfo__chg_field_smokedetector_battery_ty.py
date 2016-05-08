# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Battery'
        db.delete_table(u'smoke_detectors_battery')

        # Adding model 'BatteryInfo'
        db.create_table(u'smoke_detectors_batteryinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('number', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'smoke_detectors', ['BatteryInfo'])


        # Changing field 'SmokeDetector.battery_type'
        db.alter_column(u'smoke_detectors_smokedetector', 'battery_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smoke_detectors.BatteryInfo']))

    def backwards(self, orm):
        # Adding model 'Battery'
        db.create_table(u'smoke_detectors_battery', (
            ('type', self.gf('django.db.models.fields.CharField')(max_length=3)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'smoke_detectors', ['Battery'])

        # Deleting model 'BatteryInfo'
        db.delete_table(u'smoke_detectors_batteryinfo')


        # Changing field 'SmokeDetector.battery_type'
        db.alter_column(u'smoke_detectors_smokedetector', 'battery_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smoke_detectors.Battery']))

    models = {
        u'smoke_detectors.batteryinfo': {
            'Meta': {'object_name': 'BatteryInfo'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        u'smoke_detectors.event': {
            'Meta': {'ordering': "['date']", 'object_name': 'Event'},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'db_index': 'True'}),
            'detector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['smoke_detectors.SmokeDetector']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'smoke_detectors.location': {
            'Meta': {'ordering': "['location']", 'object_name': 'Location'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'smoke_detectors.smokedetector': {
            'Meta': {'ordering': "['location']", 'object_name': 'SmokeDetector'},
            'battery_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['smoke_detectors.BatteryInfo']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['smoke_detectors.Location']"})
        }
    }

    complete_apps = ['smoke_detectors']