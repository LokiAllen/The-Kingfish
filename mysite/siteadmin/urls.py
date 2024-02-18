from django.urls import path

from .views import *

app_name = 'siteadmin'

urlpatterns = [
    path('manageqr/', QrCodeManager.as_view(), name='manageqr'),
    path('manageqr/<str:code>/', QrCodeManager.as_view(), name='generateqrcode'),
]
