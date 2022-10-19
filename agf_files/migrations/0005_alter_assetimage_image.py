# Generated by Django 4.1 on 2022-09-15 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agf_files', '0004_alter_filemeta_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetimage',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='image_assets', to='agf_files.image'),
        ),
    ]