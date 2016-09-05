# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Bill.state'
        db.add_column(u'finances_bill', 'state',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Bill.state'
        db.delete_column(u'finances_bill', 'state')


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
        u'finances.account': {
            'Meta': {'ordering': "('name', 'statement__date')", 'object_name': 'Account'},
            'account_number': ('django.db.models.fields.PositiveIntegerField', [], {'default': "''", 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'amount': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': "'USD'"}),
            'amount_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'USD'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'statement': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['finances.Statement']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'finances.accounttemplate': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('name', 'user'),)", 'object_name': 'AccountTemplate'},
            'account_number': ('django.db.models.fields.PositiveIntegerField', [], {'default': "''", 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'disabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'finances.bill': {
            'Meta': {'ordering': "('date', 'name')", 'object_name': 'Bill'},
            'account_number': ('django.db.models.fields.PositiveIntegerField', [], {'default': "''", 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'actual': ('djmoney.models.fields.MoneyField', [], {'default_currency': "'USD'", 'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'actual_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'USD'"}),
            'amount': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': "'USD'"}),
            'amount_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'USD'"}),
            'check_number': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'options': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['finances.Option']", 'symmetrical': 'False', 'blank': 'True'}),
            'paid_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'payment_method': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'state': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'statement': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['finances.Statement']"}),
            'total': ('djmoney.models.fields.MoneyField', [], {'default_currency': "'USD'", 'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'total_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'USD'"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
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
            'options': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['finances.Option']", 'symmetrical': 'False', 'blank': 'True'}),
            'snap_section': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'total': ('djmoney.models.fields.MoneyField', [], {'default_currency': "'USD'", 'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'total_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'USD'"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'finances.income': {
            'Meta': {'ordering': "('date', 'name')", 'object_name': 'Income'},
            'account_number': ('django.db.models.fields.PositiveIntegerField', [], {'default': "''", 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'amount': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': "'USD'"}),
            'amount_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'USD'"}),
            'date': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'options': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['finances.Option']", 'symmetrical': 'False', 'blank': 'True'}),
            'statement': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['finances.Statement']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'finances.incometemplate': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('name', 'user'),)", 'object_name': 'IncomeTemplate'},
            'account_number': ('django.db.models.fields.PositiveIntegerField', [], {'default': "''", 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'amount': ('djmoney.models.fields.MoneyField', [], {'default_currency': "'USD'", 'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'amount_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'USD'"}),
            'arrival_day': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'disabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'options': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['finances.Option']", 'symmetrical': 'False', 'blank': 'True'}),
            'snap_section': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'finances.option': {
            'Meta': {'object_name': 'Option'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'template_type': ('django.db.models.fields.CharField', [], {'max_length': '7'})
        },
        u'finances.preference': {
            'Meta': {'object_name': 'Preference'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'snap_days': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '5'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'finances.statement': {
            'Meta': {'ordering': "('date',)", 'unique_together': "(('user', 'date'),)", 'object_name': 'Statement'},
            'date': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['finances']