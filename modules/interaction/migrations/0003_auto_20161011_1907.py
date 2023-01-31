# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-11 17:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('interaction', '0002_auto_20160926_0950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proteinligandinteraction',
            name='ligand',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ligand.Ligand'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='proteinligandinteraction',
            name='protein',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='protein.ProteinConformation'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='residuefragmentatom',
            name='structureligandpair',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='interaction.StructureLigandInteraction'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='residuefragmentinteraction',
            name='fragment',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='structure.Fragment'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='residuefragmentinteraction',
            name='interaction_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='interaction.ResidueFragmentInteractionType'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='residuefragmentinteraction',
            name='rotamer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='structure.Rotamer'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='residuefragmentinteraction',
            name='structure_ligand_pair',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='interaction.StructureLigandInteraction'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='structureligandinteraction',
            name='structure',
            field=models.ForeignKey(default=11, on_delete=django.db.models.deletion.CASCADE, to='structure.Structure'),
            preserve_default=False,
        ),
    ]
