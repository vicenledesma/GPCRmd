# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-10-17 18:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dynadb', '0094_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dyndbcompound',
            name='name',
            field=models.TextField(unique=True),
        ),
    ]
