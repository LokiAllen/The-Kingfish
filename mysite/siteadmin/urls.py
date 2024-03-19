from django.urls import path

from .views import *

app_name = 'siteadmin'

urlpatterns = [
    path('home/', SiteAdminHome.as_view(), name='adminhome'),
    path('manage/scores', ManageScores.as_view(), name='managescores'),
    path('manage/shop', ManageShop.as_view(), name='manageshop'),
    path('manageqr/', QrCodeManager.as_view(), name='manageqr'),
    path('manageqr/<str:code>/', QrCodeManager.as_view(), name='generateqrcode'),
]
