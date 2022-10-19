from django.shortcuts import render

from .models import *

# Create your views here.
def QuestionnairePage(request, id):
    questionnaire = Questionnaire.objects.get(id=id)
    questions = Question.objects.filter(questionnaire=questionnaire).order_by('order').all()

    context = {
        'questionnaire' : questionnaire,
        'questions' : questions,
    }

    return render(request, "agf_hse/questionnaire.html", context)

def QuestionnaireURL(request, url):
    questionnaire = Questionnaire.objects.filter(url=url).first()

    return QuestionnairePage(request, questionnaire.id)

def QuestionnaireComplete(request):
    questionnaire = Questionnaire.objects.get(id=request.POST["questionnaireID"])

    questions = []
    questionCount = 0
    qCorrect = 0

    for question in questionnaire.questions.all():
        questionCount += 1
        answers = []

        # Multiple Choice
        if question.type == Question.MULTI:
            correct = False
            for answer in question.answers.all():
                aCorrect = False
                checked = False
                answerId = "answer" + str(answer.id)
                if answer.correct:
                    try:
                        if request.POST[answerId] == "checked":
                            checked=True
                            correct = True
                            aCorrect = True
                            qCorrect += 1
                    except:
                        correct = False
                        aCorrect = False
                else:
                    try:
                        if request.POST[answerId] == "checked":
                            checked=True
                            aCorrect = False
                    except:
                        aCorrect = True
            
                answerObj = {
                    "obj" : answer,
                    "correct" : aCorrect,
                    "checked" : checked,
                }
                answers.append(answerObj)


        # Select All
        if question.type == Question.SELECT:
            correct = False
            count = 0
            countCorrect = 0
            for answer in question.answers.all():
                aCorrect = False
                checked = False
                answerId = "answer" + str(answer.id)
                if answer.correct:
                    count += 1
                    try:
                        if request.POST[answerId] == "checked":
                            checked=True
                            countCorrect += 1
                            aCorrect = True
                    except:
                        aCorrect = False
                else:
                    try:
                        if request.POST[answerId] == "checked":
                            checked=True
                            aCorrect = False
                    except:
                        aCorrect = True

                answerObj = {
                    "obj" : answer,
                    "correct" : aCorrect,
                    "checked" : checked,
                }
                answers.append(answerObj)
            
            if count == countCorrect:
                correct = True
                qCorrect += 1
            

        marked = {
            "obj" : question,
            "answers" : answers,
            "correct" : correct,
        }
        questions.append(marked)      
        
    percentage = int(round(qCorrect/questionCount*100,0))

    if percentage >= questionnaire.pass_mark:
        success = True
    else:
        success = False

    context = {
        "questionnaire" : questionnaire,
        "questions" : questions,
        "correctCount" : qCorrect,
        "questionCount" : questionCount,
        "percentage" : percentage,
        "pass" : success,
    }

    print(context)

    return render(request, "agf_hse/marked.html", context)