from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q


"""
 * Form for the login of a user, accepts both 'email' or 'username'
 * and a password
 *
 * @author Jasper
"""
class UserLogin(forms.Form):
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

"""
 * Form for the register of a user
 *
 * @author Jasper
"""
class RegisterForm(UserCreationForm):
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

"""
 * Form for changing all current information of the user
 *
 * @author Jasper
"""
class ChangeInfo(forms.Form):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    username = forms.CharField(label='Username')
    email = forms.EmailField(label='Email')
    profile_picture = forms.ImageField(required=False)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    # Gets and validates the email of the user
    def clean_email(self):
        email = self.cleaned_data['email']

        if email != self.user.email:
            user = User.objects.filter(email__iexact=email).exists()
            if user:
                raise ValidationError('An account with this email already exists')

        return email

    # Gets and validates the username of the user
    def clean_username(self):
        username = self.cleaned_data['username']

        if username != self.user.username:
            user = User.objects.filter(username__iexact=username).exists()
            if user:
                raise ValidationError('An account with this username already exists')

        return username

    # Gets and validates the first and last name of the user
    def clean_info(self):
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']

        if first_name == self.user.first_name or last_name == self.user.last_name:
            raise ValidationError('Enter a new name, not the same')

        return first_name, last_name