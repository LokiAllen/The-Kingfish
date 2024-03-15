from django.urls import path

from .views import *

app_name = 'api'

urlpatterns = [
    path('messages/<str:username>/', MessageData.as_view(), name='message_data'),
    path('data/leaderboard/<str:username>/<str:leaderboard_type>/<str:score_type>/', LeaderboardData.as_view(), name='leaderboard_data'),
    path('shop/', ShopData.as_view(), name='shop_data'),
]
