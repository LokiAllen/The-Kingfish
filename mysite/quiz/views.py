from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
import random
from .models import *
from accounts.models import UserInfo

#Author: Tom

#Render page for answering the quiz.
def QuizAttempt(request):
    user = request.user #Get session user.
    questions = getQuestions(user) #Generate random 3 questions from pool.

    #Render error page if not enough questions left for this user.
    #To be replaced with functionality to refill the pools of questions for a user.
    if(questions == []):
        return render(request, 'quiz/quiz_error.html')
    
    answers = getAnswers(questions) #Get answers for the questions.
    
    #Render the quiz with the generated question and answer arrays.
    return render(request, 'quiz/quiz_attempt.html', {'questions':questions,'answers':answers})

def QuizResult(request):
    user = request.user
    if request.method == 'POST':
        #Fetch the user's answer choices from post request.
        chosen_answerID1 = request.POST.get("chosen_answerID1", "")
        chosen_answerID2 = request.POST.get("chosen_answerID2", "")
        chosen_answerID3 = request.POST.get("chosen_answerID3", "")

        #Get the corresponding answer model objects.
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
    if len(unansweredQuestions) < 3: #If not enough questions in user's pool, reset the question pool.
        UserAnsweredQuestion.objects.filter(user = user.id).delete()
        unansweredQuestions = [q for q in allQuestions]
    questions = random.sample(unansweredQuestions, k=3)
    return questions

#Get the answers corresponding to the selected questions.
def getAnswers(questions):
    answers = [ [a for a in Answer.objects.filter(question = q)] for q in questions]
    return answers


    