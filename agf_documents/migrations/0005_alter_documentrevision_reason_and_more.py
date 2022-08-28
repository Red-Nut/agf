# Generated by Django 4.1 on 2022-08-26 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agf_documents', '0004_document_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentrevision',
            name='reason',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Draft'), (2, 'Issue for Review'), (3, 'Issue for Construction'), (4, 'Issue for Demolition'), (5, 'Issue for Tender'), (6, 'Issue for Quotation'), (7, 'Issue for Information'), (9, 'Issue for HAZOP'), (99, 'As Built')], null=True),
        ),
        migrations.AlterField(
            model_name='documentrevision',
            name='revision',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
