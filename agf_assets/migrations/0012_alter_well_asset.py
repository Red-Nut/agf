# Generated by Django 4.1 on 2022-11-29 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agf_assets', '0011_well'),
    ]

    operations = [
        migrations.AlterField(
            model_name='well',
            name='asset',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='well_details', to='agf_assets.asset'),
        ),
    ]
