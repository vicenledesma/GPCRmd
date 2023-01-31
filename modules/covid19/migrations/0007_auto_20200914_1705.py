# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2020-09-14 15:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('covid19', '0006_auto_20200821_1047'),
    ]

    operations = [
        migrations.CreateModel(
            name='CovidProtein',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uniprotkbac', models.CharField(blank=True, max_length=10, null=True)),
                ('name', models.TextField()),
                ('creation_timestamp', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'covid_protein',
                'managed': True,
            },
        ),
        migrations.RenameField(
            model_name='coviddynamics',
            old_name='author_name',
            new_name='author_first_name',
        ),
        migrations.AddField(
            model_name='coviddynamics',
            name='author_institution',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='coviddynamics',
            name='author_last_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='coviddynamicscomponents',
            name='ligand_type',
            field=models.SmallIntegerField(choices=[(0, 'None'), (1, 'Orthosteric'), (2, 'Allosteric')], default=0),
        ),
        migrations.AddField(
            model_name='coviddynamicscomponents',
            name='molecule_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='covidmodel',
            name='id_protein',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='covid19.CovidProtein'),
        ),
    ]
