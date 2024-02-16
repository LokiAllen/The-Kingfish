from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User

# Form at the url /login/ - Asks for 'username' and 'password'
class NewAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

# Form at the url /register/ - Asks for the following 6 informations
class NewUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']