# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Option'
        db.create_table(u'finances_option', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('template_type', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'finances', ['Option'])

        # Deleting field 'BillTemplate.options'
        db.delete_column(u'finances_billtemplate', 'options')

        # Adding M2M table for field options on 'BillTemplate'
        m2m_table_name = db.shorten_name(u'finances_billtemplate_options')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('billtemplate', models.ForeignKey(orm[u'finances.billtemplate'], null=False)),
            ('option', models.ForeignKey(orm[u'finances.option'], null=False))
        ))
        db.create_unique(m2m_table_name, ['billtemplate_id', 'option_id'])


    def backwards(self, orm):
        # Deleting model 'Option'
        db.delete_table(u'finances_option')

        # Adding field 'BillTemplate.options'
        db.add_column(u'finances_billtemplate', 'options',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0, blank=True),
                      keep_default=False)

        # Removing M2M table for field options on 'BillTemplate'
        db.delete_table(db.shorten_name(u'finances_billtemplate_options'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'finances.accounttemplate': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('name', 'user'),)", 'object_name': 'AccountTemplate'},
            'account_number': ('django.db.models.fields.PositiveIntegerField', [], {'default': "''", 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'disabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'finances.billtemplate': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('name', 'user'),)", 'object_name': 'BillTemplate'},
            'account_number': ('django.db.models.fields.PositiveIntegerField', [], {'default': "''", 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'amount': ('djmoney.models.fields.MoneyField', [], {'default_currency': "'USD'", 'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'amount_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'USD'"}),
            'disabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'due_day': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'options': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['finances.Option']", 'symmetrical': 'False'}),
            'total': ('djmoney.models.fields.MoneyField', [], {'default_currency': "'USD'", 'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'total_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'USD'"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'finances.option': {
            'Meta': {'object_name': 'Option'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'template_type': ('django.db.models.fields.CharField', [], {'max_length': '7'})
        }
    }

    complete_apps = ['finances']