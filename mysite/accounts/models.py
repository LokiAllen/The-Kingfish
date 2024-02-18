from django.db import models
from django.contrib.auth.models import User

# Builds from the default 'User' model to allow storing more info easily - ATM only adds 'coins'
class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user_info'