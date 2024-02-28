from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
import random
from .models import *
from accounts.models import UserInfo


def QuizAttempt(request):
    user = request.user
    questions = getQuestions(user)
    if(questions == []):
        return render(request, 'quiz/quiz_error.html')
    answers = getAnswers(questions)
    
    return render(request, 'quiz/quiz_attempt.html', {'questions':questions,'answers':answers})

def QuizResult(request):
    user = request.user
    if request.method == 'POST':
        chosen_answerID1 = request.POST.get("chosen_answerID1", "")
        chosen_answerID2 = request.POST.get("chosen_answerID2", "")
        chosen_answerID3 = request.POST.get("chosen_answerID3", "")

        chosen_answer1 = Answer.objects.get(pk=chosen_answerID1)
        chosen_answer2 = Answer.objects.get(pk=chosen_answerID2)
        chosen_answer3 = Answer.objects.get(pk=chosen_answerID3)
        chosen_answers = [chosen_answer1, chosen_answer2, chosen_answer3]
        
        score = 0

        #Increment score for each correct selected answer.
        #And register correctly answered questions for this user, so they won't be selected for the quiz again.
        for i in range(0,3):
            if(chosen_answers[i].correct == True):
                score += 1
                aq = UserAnsweredQuestion(question = chosen_answers[i].question, user = user)
                try:
                    aq.save()
                except:
                    continue
        
        
        userI = UserInfo.objects.get(user=user)
        userI.coins += score #Player gets one coin per correct answer
        userI.save()

        result_text = "You scored: "+str(score)+" out of 3!"
        
    return render(request, 'quiz/quiz_result.html', {'result_text':result_text, 'score':score})

#Retreive all questions that have not been answered correctly by the user yet.
def getQuestions(user):
    allQuestions = Question.objects.all()
    answered = UserAnsweredQuestion.objects.filter(user = user.id)
    answeredQuestions = [aq.question for aq in answered ]

    unansweredQuestions = [q for q in allQuestions if q not in answeredQuestions]
    if len(unansweredQuestions) < 3:
        return []
    questions = random.sample(unansweredQuestions, k=3)
    return questions

#Get the answers corresponding to the selected questions.
def getAnswers(questions):
    answers = [ [a for a in Answer.objects.filter(question = q)] for q in questions]
    return answers


    