from pickle import FALSE
from django.shortcuts import render
from django.core.mail import EmailMessage

from .models import *

# Create your views here.
def QuestionnairePage(request, id):

    if request.method != "POST":
        questionnaire = Questionnaire.objects.get(id=id)
        questions = Question.objects.filter(questionnaire=questionnaire).order_by('order').all()

        context = {
            'new' : True,
            'questionnaire' : questionnaire,
            'questions' : questions,
        }

        return render(request, "agf_hse/questionnaire.html", context)
    else:
        questionnaire = Questionnaire.objects.get(id=request.POST["questionnaireID"])

        # Email Details
        emailBodyTop = "<p>The following induction has been completed by " + request.POST["name"] +".</p>"
        emailBody = ""
        emailSubject = "Completed: " + questionnaire.name

        emailList = []
        for user in questionnaire.emails.all():
            emailList.append(user.user.email)


        questions = []
        questionCount = 0
        qCorrect = 0

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

        emailBodyTop += f"<p><b>Score:</b> {qCorrect}/{questionCount} ({percentage}%)"
        
            
        email = EmailMessage(
            emailSubject,
            emailBodyTop + emailBody,
            "Don't Reply <james@agl188.com>",
            emailList,
            [request.POST["email"]],
            reply_to=['no-reply@agl188.com'],
        )
        email.content_subtype = 'html' # this is required because there is no plain text email message
        email.send(fail_silently=False)

        context = {
            "new" : False,
            "questionnaire" : questionnaire,
            "questions" : questions,
            "correctCount" : qCorrect,
            "questionCount" : questionCount,
            "percentage" : percentage,
            "pass" : success,
        }

        return render(request, "agf_hse/questionnaire.html", context)

def QuestionnaireURL(request, url):
    questionnaire = Questionnaire.objects.filter(url=url).first()

    return QuestionnairePage(request, questionnaire.id)

def QuestionnaireComplete(request):
    questionnaire = Questionnaire.objects.get(id=request.POST["questionnaireID"])

    # Email Details
    emailBodyTop = "<p>The following induction has been completed by " + request.POST["name"] +".</p>"
    emailBody = ""
    emailSubject = "Completed: " + questionnaire.name

    emailList = []
    for user in questionnaire.emails.all():
        emailList.append(user.user.email)


    questions = []
    questionCount = 0
    qCorrect = 0

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

    emailBodyTop += f"<p><b>Score:</b> {qCorrect}/{questionCount} ({percentage}%)"
    
        
    email = EmailMessage(
        emailSubject,
        emailBodyTop + emailBody,
        "Don't Reply <james@agl188.com>",
        emailList,
        [request.POST["email"]],
        reply_to=['no-reply@agl188.com'],
    )
    email.content_subtype = 'html' # this is required because there is no plain text email message
    email.send(fail_silently=False)

    context = {
        "questionnaire" : questionnaire,
        "questions" : questions,
        "correctCount" : qCorrect,
        "questionCount" : questionCount,
        "percentage" : percentage,
        "pass" : success,
    }

    return render(request, "agf_hse/marked.html", context)

