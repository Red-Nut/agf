# Generated by Django 4.1 on 2022-09-14 03:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agf_assets', '0008_remove_assethierachy_asset_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AssetHierachy',
        ),
    ]
