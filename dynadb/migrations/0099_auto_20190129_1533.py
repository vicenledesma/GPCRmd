# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-01-29 14:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dynadb', '0098_dyndbsubmissiondynamicsfiles_files_dynamics_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dyndbdynamicscomponents',
            name='numberofmol',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dyndbmodelcomponents',
            name='numberofmol',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
