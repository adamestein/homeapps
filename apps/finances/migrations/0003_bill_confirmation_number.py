# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-08-10 18:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0002_auto_20190309_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='confirmation_number',
            field=models.CharField(blank=True, help_text=b'Confirmation number for payment', max_length=30, null=True),
        ),
    ]
