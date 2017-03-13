# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-02-16 16:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dynadb', '0082_auto_20170215_2017'),
    ]

    operations = [
        migrations.AddField(
            model_name='dyndbcomplexmolecule',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='dyndbcompound',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='dyndbdynamics',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='dyndbmodel',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='dyndbmolecule',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='dyndbprotein',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
    ]
