from django.urls import path

from .views import *

app_name = 'api'

urlpatterns = [
    path('messages/<str:username>/', MessageData.as_view(), name='message_data'),
    path('data/leaderboard/<str:leaderboard_type>/<str:score_type>/', LeaderboardData.as_view(), name='leaderboard_data'),
    path('shop/', ShopData.as_view(), name='shop_data'),
    path('data/user/<str:username>', UserData.as_view(), name='user_data'),
    path('data/shop/', AdminShopData.as_view(), name='admin_shop_data'),
    path('data/shop/<str:item_type_id>', AdminShopData.as_view(), name='admin_shop_data'),
]
