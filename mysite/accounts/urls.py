from django.urls import path

from .views import *

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='log_in'),
    path('register/', RegisterView.as_view(), name='register'),
    path('change/password', ChangePasswordView.as_view(), name='change_password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<str:username>/', ProfileDispatch.as_view(), name='profile'),
]
