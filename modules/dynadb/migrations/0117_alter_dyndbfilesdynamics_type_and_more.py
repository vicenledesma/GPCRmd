# Generated by Django 4.1.5 on 2023-05-03 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dynadb', '0116_alter_dyndbbinding_id_alter_dyndbefficacy_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dyndbfilesdynamics',
            name='type',
            field=models.SmallIntegerField(choices=[(0, 'Input coordinates'), (1, 'Input topology'), (2, 'Trajectory'), (3, 'Parameters'), (4, 'Others'), (5, 'Protocol')], default=0),
        ),
        migrations.AlterField(
            model_name='dyndbsubmissiondynamicsfiles',
            name='type',
            field=models.SmallIntegerField(choices=[(0, 'Input coordinates'), (1, 'Input topology'), (2, 'Trajectory'), (3, 'Parameters'), (4, 'Others'), (5, 'Protocol')], default=0),
        ),
    ]
