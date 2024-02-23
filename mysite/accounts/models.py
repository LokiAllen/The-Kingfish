from django.db import models
from django.contrib.auth.models import User

# Store the users profile pictures under '/media/profile_pictures/' as user_{id}
def upload__rename(instance, filename):
    ext = filename.split('.')[-1]
    return f'media/profile_pictures/user_{instance.user.id}.{ext}'

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)
    picture = models.ImageField(default='media/default.png', upload_to=upload__rename)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user_info'

# For friends system
class UserFriends(models.Model):
    user_id = models.IntegerField()
    following_id = models.IntegerField()
    is_friend = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_friends'
        unique_together = (('user_id', 'following_id'),)