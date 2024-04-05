# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-09-14 19:46
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preference',
            name='snap_days',
            field=models.CharField(max_length=5, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z', 32), code='invalid', message='Enter only digits separated by commas.')]),
        ),
    ]