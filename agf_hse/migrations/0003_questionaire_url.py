# Generated by Django 4.1 on 2022-10-18 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agf_hse', '0002_questionaire_pass_mark_questionaire_show_marking_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionaire',
            name='url',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]