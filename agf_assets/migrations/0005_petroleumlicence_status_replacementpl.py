# Generated by Django 4.1 on 2022-08-25 23:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agf_assets', '0004_alter_petroleumlicence_extension_term'),
    ]

    operations = [
        migrations.AddField(
            model_name='petroleumlicence',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Active'), (2, 'Expired'), (3, 'Cancelled')], default=1),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='ReplacementPL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permit', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='replacement_PL', to='agf_assets.petroleumlicence')),
                ('replacement', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='previous_PL', to='agf_assets.petroleumlicence')),
            ],
        ),
    ]