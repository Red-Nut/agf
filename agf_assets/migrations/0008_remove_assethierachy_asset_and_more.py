# Generated by Django 4.1 on 2022-09-14 03:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agf_assets', '0007_asset_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assethierachy',
            name='asset',
        ),
        migrations.RemoveField(
            model_name='assethierachy',
            name='parent',
        ),
        migrations.AddField(
            model_name='assethierachy',
            name='name',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='AssetParent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, related_name='parent', to='agf_assets.asset')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='children', to='agf_assets.asset')),
            ],
        ),
    ]
