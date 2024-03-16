# game/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', game_view, name='game'),
    path('<str:filename>/', GameFileView.as_view(), name='game__get_file'),
    path('data/user/', UserData.as_view(), name='user_data'),
]
