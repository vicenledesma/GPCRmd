# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-11 18:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dynadb', '0027_dyndbprotein_id_uniprot_species'),
    ]

    operations = [
        migrations.AddField(
            model_name='dyndbmodeledresidues',
            name='segid',
            field=models.CharField(blank=True, default='', max_length=4),
        ),
        migrations.AddField(
            model_name='dyndbmodeledresidues',
            name='seq_resid_from',
            field=models.SmallIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dyndbmodeledresidues',
            name='seq_resid_to',
            field=models.SmallIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dyndbmodeledresidues',
            name='chain',
            field=models.CharField(blank=True, default='', max_length=1),
        ),
        migrations.AlterField(
            model_name='dyndbmodeledresidues',
            name='id_protein',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='dyndbmodeledresidues',
            name='pdbid',
            field=models.CharField(max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='dyndbmodeledresidues',
            name='template_id_model',
            field=models.ForeignKey(db_column='template_id_model', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='DyndbModeledResidues_template_id_protein_fky', to='dynadb.DyndbModel'),
        ),
    ]
