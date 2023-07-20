# Generated by Django 4.1 on 2023-05-03 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agf_hse', '0009_alter_questionaireemailresult_questionnaire'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionaireResults',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.DateTimeField(auto_now=True)),
                ('mark', models.IntegerField()),
                ('name', models.CharField(max_length=40)),
                ('email', models.EmailField(max_length=254)),
                ('expiry', models.DateField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='questionaireemailresult',
            name='description',
            field=models.CharField(default=1, max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questionaireemailresult',
            name='instructions',
            field=models.CharField(default=1, max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='valid_duration_days',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='QuestionaireResultsAnswers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agf_hse.answer')),
                ('questionnaireResults', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='agf_hse.questionaireresults')),
            ],
        ),
        migrations.AddField(
            model_name='questionaireresults',
            name='questionnaire',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agf_hse.questionnaire'),
        ),
    ]