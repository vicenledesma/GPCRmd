# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-09-19 16:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dynadb', '0037_auto_20160912_0103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dyndbsubmissionprotein',
            name='protein_id',
            field=models.ForeignKey(blank=True, db_column='protein_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dynadb.DyndbProtein'),
        ),
    ]
