# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-02-13 19:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dynadb', '0077_auto_20170207_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='dyndbsubmissiondynamicsfiles',
            name='filenum',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='dyndbsubmissiondynamicsfiles',
            name='framenum',
            field=models.PositiveIntegerField(default=None, null=True),
        ),
    ]
