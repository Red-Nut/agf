# Generated by Django 4.1 on 2022-10-19 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agf_hse', '0007_rename_questionaireemailresults_questionaireemailresult_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Multiple Choice'), (2, 'Select All Applicable')]),
        ),
    ]
