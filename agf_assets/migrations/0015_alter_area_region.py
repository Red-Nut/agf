# Generated by Django 4.1 on 2022-12-02 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agf_assets', '0014_area_region'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='areas', to='agf_assets.region'),
        ),
    ]
