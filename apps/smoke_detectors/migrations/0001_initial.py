# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Battery'
        db.create_table(u'smoke_detectors_battery', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('number', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'smoke_detectors', ['Battery'])

        # Adding model 'Event'
        db.create_table(u'smoke_detectors_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('detector', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smoke_detectors.SmokeDetector'])),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, db_index=True)),
        ))
        db.send_create_signal(u'smoke_detectors', ['Event'])

        # Adding model 'Location'
        db.create_table(u'smoke_detectors_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'smoke_detectors', ['Location'])

        # Adding model 'SmokeDetector'
        db.create_table(u'smoke_detectors_smokedetector', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smoke_detectors.Location'])),
            ('battery_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smoke_detectors.Battery'])),
        ))
        db.send_create_signal(u'smoke_detectors', ['SmokeDetector'])


    def backwards(self, orm):
        # Deleting model 'Battery'
        db.delete_table(u'smoke_detectors_battery')

        # Deleting model 'Event'
        db.delete_table(u'smoke_detectors_event')

        # Deleting model 'Location'
        db.delete_table(u'smoke_detectors_location')

        # Deleting model 'SmokeDetector'
        db.delete_table(u'smoke_detectors_smokedetector')


    models = {
        u'smoke_detectors.battery': {
            'Meta': {'object_name': 'Battery'},
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
            'battery_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['smoke_detectors.Battery']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['smoke_detectors.Location']"})
        }
    }

    complete_apps = ['smoke_detectors']