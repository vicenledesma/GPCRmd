# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-26 14:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dynadb', '0076_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dyndbreferences',
            name='title',
            field=models.CharField(blank=True, help_text='Title of the paper.', max_length=900, null=True, verbose_name='Title'),
        ),
    ]
