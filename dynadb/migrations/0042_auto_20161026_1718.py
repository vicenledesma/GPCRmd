# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-26 15:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dynadb', '0041_auto_20161007_2001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dyndbcomplexcompound',
            name='id_complex_exp',
            field=models.ForeignKey(db_column='id_complex_exp', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dynadb.DyndbComplexExp'),
        ),
        migrations.AlterField(
            model_name='dyndbcomplexcompound',
            name='id_compound',
            field=models.ForeignKey(db_column='id_compound', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dynadb.DyndbCompound'),
        ),
    ]
