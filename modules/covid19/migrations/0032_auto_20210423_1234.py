# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2021-04-23 10:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('covid19', '0031_auto_20210423_1233'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='covidmutfincdata',
            unique_together=set([('mutfunc_name', 'position', 'mut')]),
        ),
    ]
