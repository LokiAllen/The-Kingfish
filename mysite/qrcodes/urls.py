from django.urls import path

from .views import *

app_name = 'qrcodes'

urlpatterns = [
    path('<str:code>/', QRCodeRedeem.as_view(), name='qrcoderedeem'),
]
