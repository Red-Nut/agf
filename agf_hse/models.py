from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

from enum import unique
from nturl2path import url2pathname

# Create your models here.
class Questionnaire (models.Model):
    name=models.CharField(max_length=255)
    show_marking = models.BooleanField()
    pass_mark = models.IntegerField(validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ])
    url=models.CharField(max_length=255, null=True, blank=True, unique=True)
    description=models.CharField(max_length=1000)
    instructions=models.CharField(max_length=1000)
    valid_duration_days=models.IntegerField()

    def __str__(self):
        return f"{self.name}"

class QuestionaireEmailResult(models.Model):
    questionnaire=models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name='emails')
    user=models.ForeignKey(User, on_delete=models.CASCADE)

class Question (models.Model):
    MULTI = 1
    SELECT = 2

    TYPE = (
        (MULTI, _('Multiple Choice')),
        (SELECT, _('Select All Applicable')),
    )

    questionnaire=models.ForeignKey(Questionnaire,on_delete=models.CASCADE, related_name='questions')
    question=models.CharField(max_length=255)
    type=models.PositiveSmallIntegerField(choices=TYPE)
    order=models.IntegerField()
    
    def __str__(self):
        return f"{self.question}"

class Answer(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE, related_name='answers')
    answer=models.CharField(max_length=255)
    correct=models.BooleanField()

    def __str__(self):
        return f"{self.answer}"

class QuestionaireResults(models.Model):
    questionnaire=models.ForeignKey(Questionnaire,on_delete=models.CASCADE)
    completed=models.DateTimeField(auto_now=True)
    mark = models.IntegerField()
    passed = models.BooleanField()
    name=models.CharField(max_length=40)
    email=models.EmailField()
    expiry=models.DateField(null=True)

class QuestionaireResultsAnswers(models.Model):
    questionnaireResults=models.ForeignKey(QuestionaireResults,on_delete=models.CASCADE, related_name='answers')
    answer=models.ForeignKey(Answer,on_delete=models.RESTRICT)