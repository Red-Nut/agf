from django.contrib import admin

from .models import *



class EmailInline(admin.TabularInline):
    model = QuestionaireEmailResult
    extra=0
    verbose_name = "User"
    verbose_name_plural = "Email Results to the following users"

class QuestionInline(admin.TabularInline):
    model = Question
    fields=('question',)
    readonly_fields=('question',)
    show_change_link = True
    extra=0

class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    search_fields = ['name']
    inlines = [EmailInline, QuestionInline]
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