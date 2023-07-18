from django.contrib import admin

from .models import *



class EmailInline(admin.TabularInline):
    model = QuestionaireEmailResult
    extra=0
    verbose_name = "User"
    verbose_name_plural = "Email Results to the following users"

class QuestionInline(admin.TabularInline):
    model = Question
    fields=('order','question','type')
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



class QuestionaireResultsAnswersInline(admin.TabularInline):
    model = QuestionaireResultsAnswers
    readonly_fields = ('answer_id','answer',)
    can_delete = False
    extra=0

class QuestionaireResultsAdmin(admin.ModelAdmin):
    list_display = ['id','questionnaire', 'passed', 'expiry', 'name', 'email', 'completed', 'mark']
    search_fields = ['name','questionnaire__name']
    inlines = [QuestionaireResultsAnswersInline]
    def get_ordering(self, request):
        return ['expiry']
admin.site.register(QuestionaireResults, QuestionaireResultsAdmin)