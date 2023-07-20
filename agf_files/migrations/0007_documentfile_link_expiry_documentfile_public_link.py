# Generated by Django 4.1 on 2022-12-08 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agf_files', '0006_alter_documentfile_document_revision'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentfile',
            name='link_expiry',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='documentfile',
            name='public_link',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]