from pickle import FALSE
from django.shortcuts import render
from django.core.mail import EmailMessage

from .models import *

import datetime

# Create your views here.
def Dashboard(request):
    questionnaires = Questionnaire.objects.all()

    context = {
        'questionnaires' : questionnaires,
    }

    return render(request, "agf_hse/dashboard.html", context)

def QuestionnairePage(request, id):

        questionnaire = Questionnaire.objects.get(id=id)
        questionObjects = Question.objects.filter(questionnaire=questionnaire).order_by('order').all()

        incompleteQuestions = []
        i = 0
        for question in questionObjects:
            i += 1
            answers = []
            for answer in question.answers.all():
                answerObj = {
                    "obj" : answer,
                    "correct" : None,
                    "checked" : False,
                }
                answers.append(answerObj)

            marked = {
                "number" : i,
                "obj" : question,
                "answers" : answers,
                "correct" : None,
            }

            incompleteQuestions.append(marked)   


        context = {
            'questionnaire' : questionnaire,
            'incompleteQuestions' : incompleteQuestions,
            'completeQuestions' : None,
            "correctCount" : None,
            "questionCount" : None,
            "percentage" : None,
            "pass" : None,
            'name' : "",
            'email' : "",
            'showIncorrect' : False,
            'showCorrect' : False,
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
    emailBody = ""

    questionObjects = Question.objects.filter(questionnaire=questionnaire).order_by('order').all()

    i = 0
    for question in questionObjects:
        i += 1
        questionCount += 1
        answers = []

        # Multiple Choice
        if question.type == Question.MULTI:
            # email body
            answerText = ""

            correct = False
            for answer in question.answers.all():
                # email body
                answerText += "<tr><td></td>"

                aCorrect = False
                checked = False
                answerId = "answer" + str(answer.id)
                if answer.correct:
                    try:
                        if request.POST[answerId] == "checked":
                            # email body
                            answerText += "<td style='text-align:center; color:green;'><b>&#10003;</b></td>"
                            answerText+="<td><b>" + str(answer.answer) + "</b></td></tr>"

                            checked=True
                            correct = True
                            aCorrect = True
                            qCorrect += 1
                    except:
                        # email body
                        answerText += "<td style='text-align:center;color:red;'><b>-</b></td>"
                        answerText+="<td><b>" + str(answer.answer) + "</b></td></tr>"

                        correct = False
                        aCorrect = False
                else:
                    try:
                        if request.POST[answerId] == "checked":
                            # email body
                            answerText += "<td style='text-align:center;color:red;'><b>&#215;</b></td>"
                            answerText+="<td>" + str(answer.answer) + "</td></tr>"

                            checked=True
                            aCorrect = False
                    except:
                        # email body
                        answerText += "<td style='text-align:center;'><b>-</b></td>"
                        answerText+="<td>" + str(answer.answer) + "</td></tr>"

                        aCorrect = True
            
                answerObj = {
                    "obj" : answer,
                    "correct" : aCorrect,
                    "checked" : checked,
                }
                answers.append(answerObj)

            emailBody += "<br><table><tr><td colspan=3><b>"
            if correct:
                emailBody += "<i style='color:green'>&#10003;</i>"
            else:
                emailBody += "<i style='color:red'>&#215;</i>"
            emailBody += "   Question " + str(i) + "</b> (" + question.get_type_display() + ")</td></tr>"
            emailBody += "<tr><td></td><td colspan=2>" + str(question.question) + "</tr>"
            emailBody += answerText
                


        # Select All
        if question.type == Question.SELECT:
            # email body
            answerText = ""
            
            correct = False
            count = 0
            countCorrect = 0
            for answer in question.answers.all():
                # email body
                answerText += "<tr><td></td>"
                
                aCorrect = False
                checked = False
                answerId = "answer" + str(answer.id)
                if answer.correct:
                    count += 1
                    try:
                        if request.POST[answerId] == "checked":
                            # email body
                            answerText += "<td style='text-align:center; color:green;'><b>&#10003;</b></td>"
                            answerText+="<td><b>" + str(answer.answer) + "</b></td></tr>"

                            checked=True
                            countCorrect += 1
                            aCorrect = True
                    except:
                        # email body
                        answerText += "<td style='text-align:center;color:red;'><b>-</b></td>"
                        answerText+="<td><b>" + str(answer.answer) + "</b></td></tr>"
                        aCorrect = False
                else:
                    try:
                        if request.POST[answerId] == "checked":
                            # email body
                            answerText += "<td style='text-align:center;color:red;'><b>&#10003;</b></td>"
                            answerText+="<td>" + str(answer.answer) + "</td></tr>"

                            count = 9999
                            checked=True
                            aCorrect = False
                    except:
                        # email body
                        answerText += "<td style='text-align:center;'><b>-</b></td>"
                        answerText+="<td>" + str(answer.answer) + "</td></tr>"

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

            emailBody += "<table><tr><td colspan=3><b>"
            if correct:
                emailBody += "<i style='color:green'>&#10003;</i>"
            else:
                emailBody += "<i style='color:red'>&#215;</i>"
            emailBody += "   Question " + str(i) + "</b> (" + question.get_type_display() + ")</td></tr>"
            emailBody += "<tr><td></td><td colspan=2>" + str(question.question) + "</tr>"
            emailBody += answerText
            

        marked = {
            "obj" : question,
            "answers" : answers,
            "correct" : correct,
        }
        questions.append(marked)    

        emailBody += "</table>"  
        
    percentage = int(round(qCorrect/questionCount*100,0))

    if percentage >= questionnaire.pass_mark:
        success = True
    else:
        success = False

    emailSuccess = EmailResults(request.POST["name"], [request.POST["email"]], emailBody, questionnaire, qCorrect, questionCount, percentage)

    # Save results
    if success:
        expiryDate = datetime.datetime.now() + datetime.timedelta(days=questionnaire.valid_duration_days)
    else:
        expiryDate = None

    results = QuestionaireResults.objects.create(
        questionnaire = questionnaire,
        mark = percentage,
        passed = success,
        name = request.POST["name"],
        email = [request.POST["email"]],
        expiry = expiryDate
    )

    for question in questions:
        for answer in question['answers']:
            if answer["checked"] == True:
                answerObj = Answer.objects.get(id=answer["obj"].id)
                if answerObj is not None:
                    QuestionaireResultsAnswers.objects.create(
                        questionnaireResults = results,
                        answer = answerObj
                    )

    context = {
        "questionnaire" : questionnaire,
        "questions" : questions,
        "correctCount" : qCorrect,
        "questionCount" : questionCount,
        "percentage" : percentage,
        "pass" : success,
        "name" : request.POST["name"],
        "email" : [request.POST["email"]],
        "expiry" : expiryDate,
        "emailSuccess" : emailSuccess,
    }

    return render(request, "agf_hse/marked.html", context)

def QuestionnaireResults(request, id):
    results = QuestionaireResults.objects.get(id=id)
    questionnaire = results.questionnaire
    questionObjects = Question.objects.filter(questionnaire=questionnaire).order_by('order').all()

    questions = []
    questionCount = 0
    qCorrect = 0

    for question in questionObjects:
        questionCount += 1
        answers = []

        # Multiple Choice
        if question.type == Question.MULTI:

            correct = False
            for answer in question.answers.all():
                aCorrect = False
                checked = False
                if answer.correct:
                    for a in results.answers.all():
                        if a.answer.id == answer.id:
                            checked=True
                            correct = True
                            aCorrect = True
                            qCorrect += 1
                else:
                    for a in results.answers.all():
                        if a.answer.id == answer.id:
                            checked=True
                            aCorrect = False
            
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
                if answer.correct:
                    count += 1
                    for a in results.answers.all():
                        if a.answer.id == answer.id:
                            checked=True
                            countCorrect += 1
                            aCorrect = True
                else:
                    aCorrect = True
                    for a in results.answers.all():
                        if a.answer.id == answer.id:
                            count = 9999
                            checked=True
                            aCorrect = False

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

    email = results.email
    email = email.replace("[",'')
    email = email.replace("]",'')
    email = email.replace("'",'')

    context = {
            "questionnaire" : questionnaire,
            "questions" : questions,
            "correctCount" : qCorrect,
            "questionCount" : questionCount,
            "percentage" : percentage,
            "pass" : success,
            "name" : results.name,
            "email" : email,
            "expiry" : results.expiry,
            "emailSuccess" : True,
        }

    return render(request, "agf_hse/marked.html", context)

def EmailResults(name, toEmail, emailBody, questionnaire, qCorrect, questionCount, percentage):
    print("start email")
    try:
        # Email Details
        emailBodyTop = "<p>The following induction has been completed by " + name +".</p>"
        emailSubject = "Completed: " + questionnaire.name

        emailList = []
        for user in questionnaire.emails.all():
            emailList.append(user.user.email)

        emailBodyTop += f"<p><b>Score:</b> {qCorrect}/{questionCount} ({percentage}%)"        
            
        email = EmailMessage(
            emailSubject,
            emailBodyTop + emailBody,
            "Don't Reply <james@agl188.com>",
            #"james@agl188.com",
            emailList,
            cc=toEmail,
            reply_to=['no-reply@agl188.com'],
        )
        email.content_subtype = 'html' # this is required because there is no plain text email message
        email.send(fail_silently=False)
        print("email success")

        return True
    except Exception as e:
        print(e)
        print("email failed")
        return False

