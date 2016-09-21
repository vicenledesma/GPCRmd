# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-11 22:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dynadb', '0033_auto_20160911_2203'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dyndbfilesmolecule',
            options={'managed': True},
        ),
        migrations.AlterField(
            model_name='dyndbfilesdynamics',
            name='type',
            field=models.SmallIntegerField(choices=[(0, 'Input coordinates'), (1, 'Input topology'), (2, 'Trajectory'), (3, 'Others')], default=0),
        ),
    ]
