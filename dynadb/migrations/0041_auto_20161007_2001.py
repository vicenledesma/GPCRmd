# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-10-07 18:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dynadb', '0040_auto_20160921_2042'),
    ]

    operations = [
        migrations.AddField(
            model_name='dyndbdynamics',
            name='delta',
            field=models.FloatField(default=0.1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dyndbdynamics',
            name='timestep',
            field=models.FloatField(default=4),
            preserve_default=False,
        ),
    ]
