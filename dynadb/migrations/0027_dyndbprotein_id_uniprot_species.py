# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-17 22:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dynadb', '0026_auto_20160818_0008'),
    ]

    operations = [
        migrations.AddField(
            model_name='dyndbprotein',
            name='id_uniprot_species',
            field=models.ForeignKey(db_column='id_uniprot_species', default=11463, on_delete=django.db.models.deletion.DO_NOTHING, to='dynadb.DyndbUniprotSpecies'),
            preserve_default=False,
        ),
    ]
