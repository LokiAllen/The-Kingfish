from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_message')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_message')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_messages'
        ordering = ['-timestamp']