# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-15 12:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='authors',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='journal',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='common.PublicationJournal'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='reference',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='title',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='year',
            field=models.IntegerField(null=True),
        ),
    ]
