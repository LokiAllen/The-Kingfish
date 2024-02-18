from django.urls import path

from .views import *

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='log_in'),
    path('register/', RegisterView.as_view(), name='register'),
    path('change/email', ChangeEmailView.as_view(), name='change_email'),
    path('change/username', ChangeUsernameView.as_view(), name='change_username'),
    path('change/password', ChangePasswordView.as_view(), name='change_password'),
    path('change/info', ChangeInfoView.as_view(), name='change_info'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
