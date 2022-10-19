from django.contrib import admin

from .models import *

# Register your models here.
class EmailInline(admin.TabularInline):
    model = QuestionaireEmailResult

class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    search_fields = ['name']
    inlines = [EmailInline]
    def get_ordering(self, request):
        return ['id']
admin.site.register(Questionnaire, QuestionnaireAdmin)



class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id','questionnaire', 'order', 'question', 'type']
    search_fields = ['question','questionnaire__name']
    inlines = [AnswerInline]
    def get_ordering(self, request):
        return ['questionnaire', 'order']
admin.site.register(Question, QuestionAdmin)