# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2021-07-03 10:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('covid19', '0041_auto_20210703_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='covidisolate',
            name='isolate_id',
            field=models.CharField(default='-', max_length=100, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='covidsequencedgene',
            name='id_isolate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='covid19.CovidIsolate'),
        ),
    ]
