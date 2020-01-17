# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2020-01-15 10:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dynadb', '0102_auto_20200115_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dyndbreferences',
            name='doi',
            field=models.CharField(blank=True, help_text='Digital object identifier.', max_length=80, null=True, unique=True, verbose_name='DOI'),
        ),
        migrations.AlterField(
            model_name='dyndbreferences',
            name='pmid',
            field=models.IntegerField(blank=True, help_text='PubMed identifier or PubMed unique identifier', null=True, unique=True, verbose_name='PMID'),
        ),
    ]
