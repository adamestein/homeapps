# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-01-01 20:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BatteryChangeEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(db_index=True, default=datetime.date.today, help_text='Battery change date')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='BatteryInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('9v', '9 volt'), ('AA', 'AA'), ('AAA', 'AAA'), ('C', 'C'), ('D', 'D')], help_text='Battery Type', max_length=3)),
                ('number', models.PositiveSmallIntegerField(help_text='Number of batteries required by this smoke detector')),
            ],
            options={
                'verbose_name_plural': 'Batteries',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(help_text='Location of detector', max_length=50)),
            ],
            options={
                'ordering': ['location'],
            },
        ),
        migrations.CreateModel(
            name='SmokeDetector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('battery_type', models.ForeignKey(help_text='Type of battery the smoke detector uses', on_delete=django.db.models.deletion.CASCADE, to='smoke_detectors.BatteryInfo')),
                ('location', models.ForeignKey(help_text='Location of the smoke detector', on_delete=django.db.models.deletion.CASCADE, to='smoke_detectors.Location')),
            ],
            options={
                'ordering': ['location'],
            },
        ),
        migrations.AddField(
            model_name='batterychangeevent',
            name='detector',
            field=models.ForeignKey(help_text='Smoke detector this event is for', on_delete=django.db.models.deletion.CASCADE, to='smoke_detectors.SmokeDetector'),
        ),
    ]
