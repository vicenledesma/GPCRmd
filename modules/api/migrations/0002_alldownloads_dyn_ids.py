# Generated by Django 4.1.5 on 2023-05-03 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='alldownloads',
            name='dyn_ids',
            field=models.CharField(default=0, max_length=1000, unique=True),
            preserve_default=False,
        ),
    ]
