from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

"""
 New user model 
 - May require changing but for now a new one is set, mainly to allow 'coins' so the QRCode scan functions
 - Note: This overrides the django 'AUTH_USER' model and changing it is difficult and may require changing
         other areas regarding the login page, talk to Jasper about making any changes to the model
"""
# The managing of the user models in creating and deleting both normal and super users
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

# The model itself
class User(AbstractBaseUser, PermissionsMixin):
    # Basically just the database attributes
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    coins = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    """ USERNAME_FIELD means that logging in requires 'username' as the identifier other than password 
            - For example changing to 'email' would require them logging in with email and password """

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    # Sets the database name to 'user' instead of 'mysite.login.user'
    class Meta:
        db_table = 'user'