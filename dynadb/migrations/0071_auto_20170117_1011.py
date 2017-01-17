# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-17 09:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dynadb', '0070_auto_20170107_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dyndbreferences',
            name='authors',
            field=models.CharField(blank=True, help_text='List of the authors separated by semicolon.', max_length=600, null=True, verbose_name='Authors'),
        ),
    ]
