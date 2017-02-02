# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-26 17:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dynadb', '0075_auto_20170125_1836'),
    ]

    operations = [
        migrations.AddField(
            model_name='dyndbmodel',
            name='model_creation_submission_id',
            field=models.ForeignKey(blank=True, db_column='model_creation_submission_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dynadb.DyndbSubmission', unique=True),
        ),
        migrations.AddField(
            model_name='dyndbmolecule',
            name='molecule_creation_submission_id',
            field=models.ForeignKey(blank=True, db_column='molecule_creation_submission_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dynadb.DyndbSubmission'),
        ),
        migrations.AddField(
            model_name='dyndbprotein',
            name='protein_creation_submission_id',
            field=models.ForeignKey(blank=True, db_column='protein_creation_submission_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dynadb.DyndbSubmission'),
        ),
    ]
