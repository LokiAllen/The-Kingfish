from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q

from .models import Titles, UserOwnedTitles, UserOwnedBackgrounds, Backgrounds

class UserLogin(forms.Form):
    """
     * Form for the login of a user, accepts both 'email' or 'username'
     * and a password
     *
     * @author Jasper
    """
    username_or_email = forms.CharField(label='Username or Email')
    password = forms.CharField(label='Password', strip=False, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username_or_email', 'password']

    def __init__(self, *args, **kwargs):
        self.user = None
        super().__init__(*args, **kwargs)

    # Cleans and validates the username/email
    def clean_username_or_email(self):
        username_or_email = self.cleaned_data['username_or_email']

        # Checks whether there exists a user with the username or email that they have entered
        user = User.objects.filter(Q(username__iexact=username_or_email) | Q(email__iexact=username_or_email)).first()

        if not user:
            raise ValidationError('User does not exist')

        if not user.is_active:
            raise ValidationError('Account is not active')

        # Sets user to be used in the clean_password validation check
        self.user = user

        return username_or_email

    # Cleans and validates the password
    def clean_password(self):
        password = self.cleaned_data['password']

        if self.user and not self.user.check_password(password):
            raise ValidationError('Incorrect password')

        return password

class RegisterForm(UserCreationForm):
    """
     * Form for the register of a user
     *
     * @author Jasper
    """
    profile_picture = forms.ImageField(required=False)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'profile_picture']

    # Gets (if exists) and validates the username of the user
    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError('An account with this username already exists')

        return username

    # Gets (if exists) and validates the email of the user
    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('An account with this email already exists')

        return email

class ChangeInfo(forms.Form):
    """
     * Form for changing all current information of the user
     *
     * @author Jasper
    """
    first_name = forms.CharField(label='First Name', required=False)
    last_name = forms.CharField(label='Last Name', required=False)
    username = forms.CharField(label='Username', required=False)
    email = forms.EmailField(label='Email', required=False)
    profile_picture = forms.ImageField(required=False)
    title = forms.ChoiceField(label='Titles', choices=[], required=False)
    background = forms.ChoiceField(label='Backgrounds', choices=[], required=False)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

        titles = UserOwnedTitles.objects.filter(user=self.user)
        backgrounds = UserOwnedBackgrounds.objects.filter(user=self.user)
        self.fields['title'].choices = [(title.title.id, title.title.title_name) for title in titles]
        self.fields['background'].choices = [(background.background.id, background.background.background_name) for background in backgrounds]

    # Gets and validates the email of the user
    def clean_email(self):
        email = self.cleaned_data['email']

        if not email:
            return self.user.email

        if email != self.user.email:
            user = User.objects.filter(email__iexact=email).exists()
            if user:
                raise ValidationError('An account with this email already exists')

        return email

    # Gets and validates the username of the user
    def clean_username(self):
        username = self.cleaned_data['username']

        if not username:
            return self.user.username

        if username != self.user.username:
            user = User.objects.filter(username__iexact=username).exists()
            if user:
                raise ValidationError('An account with this username already exists')

        return username

    # Gets and validates the first and last name of the user
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']

        if not first_name:
            first_name = self.user.first_name

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']

        if not last_name:
            last_name = self.user.last_name

        return last_name

    def clean_title(self):
        title = self.cleaned_data['title']

        if not title:
            return self.user.title

        user_owned_titles = UserOwnedTitles.objects.filter(user=self.user, title=title)
        if not user_owned_titles:
            raise ValidationError('You do not own this title')

        title_object = Titles.objects.filter(id=title)
        if not title_object:
            raise ValidationError('Title does not exist')

        return title_object.first()

    def clean_background(self):
        background = self.cleaned_data['background']

        if not background:
            return self.user.background

        user_owned_backgrounds = UserOwnedBackgrounds.objects.filter(user=self.user, background=background)
        if not user_owned_backgrounds:
            raise ValidationError('You do not own this title')

        background_object = Backgrounds.objects.filter(id=background)
        if not background_object:
            raise ValidationError('Title does not exist')

        return background_object.first()