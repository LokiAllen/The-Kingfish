from django.urls import path

from . import views

"""
    - Any url at qrcodes/(code) will have the same effect, and will do something based on the (code) entered
    - location/ is used to send a request to verify the location and validity of the code
"""
urlpatterns = [
    path("<str:code>", views.qrcode_scan, name="scan_code"),
    path("location/<str:code>", views.get_location, name="location_check"),
]