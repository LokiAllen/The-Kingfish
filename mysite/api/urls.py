from django.urls import path

from .views import *

app_name = 'api'

urlpatterns = [
    path('messages/<str:username>/', MessageData.as_view(), name='message_data'),
    path('data/user/', UserData.as_view(), name='user_data'),
]
