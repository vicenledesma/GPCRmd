# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-19 14:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dynadb', '0021_auto_20160719_1641'),
    ]

    operations = [
#       migrations.AddField(
#           model_name='dyndbprotein',
#           name='id_species',
#           field=models.ForeignKey(blank=True, db_column='id_species', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dynadb.Species'),
#       ),
#       migrations.AddField(
#           model_name='dyndbprotein',
#           name='receptor_id_protein',
#           field=models.ForeignKey(blank=True, db_column='receptor_id_protein', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dynadb.DyndbProtein'),
#       ),
        migrations.AlterField(
            model_name='dyndbprotein',
            name='update_timestamp',
            field=models.DateTimeField(null=True),
        ),
    ]
