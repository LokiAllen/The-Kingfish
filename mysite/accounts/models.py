from django.db import models
from django.contrib.auth.models import User

class Titles(models.Model):
    """
     * Stores all currently available titles
     *
     * @author Jasper
    """
    title_name = models.TextField(unique=True)
    title_description = models.TextField()

    class Meta:
        db_table = 'user_titles'

class Backgrounds(models.Model):
    """
     * Stores all currently available backgrounds
     *
     * @author Jasper
    """
    background_name = models.TextField(unique=True)
    background_description = models.TextField()
    picture = models.ImageField(default=None, null=True)
    # Added css_class for if in the future we want to change the css properties of the background instead of an image
    css_class = models.TextField(default=None, null=True)

    class Meta:
        db_table = 'user_backgrounds'

class UserOwnedTitles(models.Model):
    """
     * Stores the titles that each user owns
     *
     * @author Jasper
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_owned_titles'
        unique_together = ('user', 'title')

class UserOwnedBackgrounds(models.Model):
    """
     * Stores the backgrounds that each user owns
     *
     * @author Jasper
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    background = models.ForeignKey(Backgrounds, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_owned_backgrounds'
        unique_together = ('user', 'background')


def upload__rename(instance, filename):
    """
        Store the users profile pictures under '/media/profile_pictures/' as user_{id}

        @param instance: The current user instance
        @param filename: The file name of the file uploaded
        @return The new file path of the file uploaded
    """
    ext = filename.split('.')[-1]
    return f'media/profile_pictures/user_{instance.user.id}.{ext}'

class UserInfo(models.Model):
    """
     * Model for storing additional information for users
     *
     * @author Jasper and Loki
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)
    highscore = models.IntegerField(default=0)
    cumulativeScore = models.IntegerField(default=0)
    picture = models.ImageField(default='media/default.png', upload_to=upload__rename)
    title = models.ForeignKey(Titles, on_delete=models.SET_DEFAULT, default=1)
    background = models.ForeignKey(Backgrounds, on_delete=models.SET_DEFAULT, default=1)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'user_info'

class UserFriends(models.Model):
    """
     * Model for storing information for friends of users
     *
     * @author Jasper
    """
    user_id = models.IntegerField()
    following_id = models.IntegerField()
    is_friend = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_friends'
        unique_together = (('user_id', 'following_id'),)


