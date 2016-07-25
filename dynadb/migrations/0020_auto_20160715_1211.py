# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-15 10:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dynadb', '0019_auto_20160715_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='dyndbproteinmutations',
            name='id_protein',
            field=models.ForeignKey(db_column='id_protein', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dynadb.DyndbProtein'),
        ),
        migrations.AlterModelOptions(
            name='dyndbfiles',
            options={'managed':False},
        ),
        migrations.AlterField(
            model_name='dyndbproteinmutations',
            name='id_protein',
            field=models.ForeignKey(db_column='id_protein', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dynadb.DyndbProtein'),
        ),
        migrations.AlterField(
            model_name='dyndbproteinmutations',
            name='resid',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='dyndbproteinmutations',
            name='resletter_from',
            field=models.CharField(max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='dyndbproteinmutations',
            name='resletter_to',
            field=models.CharField(max_length=1, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='dyndbproteinmutations',
            unique_together=set([('id_protein', 'resid', 'resletter_from', 'resletter_to')]),
        ),
    ]
