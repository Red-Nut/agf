# Generated by Django 4.1 on 2023-07-18 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agf_maintenance', '0014_alter_wotask_options_alter_proceduretask_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wotask',
            name='task',
            field=models.CharField(max_length=9999),
        ),
    ]
