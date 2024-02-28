from django.db import models
from accounts.models import UserInfo
from django.contrib.auth.models import User

class Question(models.Model):
    q_text = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.q_text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    a_text = models.CharField(max_length=100)
    label = models.CharField(max_length=1)
    correct = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.a_text
    
class UserAnsweredQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('question', 'user'))