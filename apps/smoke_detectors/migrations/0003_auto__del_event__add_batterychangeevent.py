# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Event'
        db.delete_table(u'smoke_detectors_event')

        # Adding model 'BatteryChangeEvent'
        db.create_table(u'smoke_detectors_batterychangeevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('detector', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smoke_detectors.SmokeDetector'])),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, db_index=True)),
        ))
        db.send_create_signal(u'smoke_detectors', ['BatteryChangeEvent'])


    def backwards(self, orm):
        # Adding model 'Event'
        db.create_table(u'smoke_detectors_event', (
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, db_index=True)),
            ('detector', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smoke_detectors.SmokeDetector'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'smoke_detectors', ['Event'])

        # Deleting model 'BatteryChangeEvent'
        db.delete_table(u'smoke_detectors_batterychangeevent')


    models = {
        u'smoke_detectors.batterychangeevent': {
            'Meta': {'ordering': "['date']", 'object_name': 'BatteryChangeEvent'},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'db_index': 'True'}),
            'detector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['smoke_detectors.SmokeDetector']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'smoke_detectors.batteryinfo': {
            'Meta': {'object_name': 'BatteryInfo'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '3'})
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