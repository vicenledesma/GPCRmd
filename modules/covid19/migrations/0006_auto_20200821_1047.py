# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2020-08-21 08:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('covid19', '0005_auto_20200818_1241'),
    ]

    operations = [
        migrations.CreateModel(
            name='CovidDynamicsComponents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resname', models.CharField(max_length=4)),
                ('numberofmol', models.PositiveIntegerField(blank=True, null=True)),
                ('creation_timestamp', models.DateField(default=django.utils.timezone.now)),
                ('is_ligand', models.BooleanField(default=False)),
            ],
            options={
                'managed': True,
                'db_table': 'covid_dynamics_components',
            },
        ),
        migrations.AddField(
            model_name='coviddynamics',
            name='delta',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='coviddynamicscomponents',
            name='id_dynamics',
            field=models.ForeignKey(db_column='id_dynamics', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='covid19.CovidDynamics'),
        ),
        migrations.AlterUniqueTogether(
            name='coviddynamicscomponents',
            unique_together=set([('id_dynamics', 'resname')]),
        ),
    ]
