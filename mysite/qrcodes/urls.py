from django.urls import path

from .views import *

app_name = 'qrcodes'

urlpatterns = [
    path('interactive-map/', interactive_map, name='interactive_map'),
    path('<str:code>/', QRCodeRedeem.as_view(), name='qrcoderedeem'),
]
