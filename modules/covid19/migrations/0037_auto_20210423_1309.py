# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2021-04-23 11:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid19', '0036_auto_20210423_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='covidmutfuncdatainterface',
            name='int_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
