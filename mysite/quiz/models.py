from django.db import models
from accounts.models import UserInfo
from django.contrib.auth.models import User

#Author: Tom

class Question(models.Model):
    q_text = models.CharField(max_length=100) #Text of the question.

    def __str__(self) -> str:
        return self.q_text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE) #Corresponding question.
    a_text = models.CharField(max_length=100) #Text of the answer option
    correct = models.BooleanField(default=False) #Boolean value of whether the option is correct.

    def __str__(self) -> str:
        return self.a_text
    
#Keep track of which users have already answered certain questions correctly.
class UserAnsweredQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    #Make sure each combination of a question and user is unique.
    class Meta:
        unique_together = (('question', 'user'))