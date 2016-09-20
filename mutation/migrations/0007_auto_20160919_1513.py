# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-19 13:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('protein', '0003_auto_20160916_1928'),
        ('residue', '0001_initial'),
        ('mutation', '0006_auto_20160919_1511'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='mutation',
            unique_together=set([('protein', 'residue', 'amino_acid')]),
        ),
    ]
