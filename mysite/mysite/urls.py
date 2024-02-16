"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from mysite import views as main_views
from login import views as login_views
from qrcodes import views as qr_views

urlpatterns = [
    path("polls/", include("polls.urls")),
    path("old_admin/", admin.site.urls), # Changed to old_admin to allow the start of creating a new admin page (can be reverted easily)
    path("login/", login_views.login_view, name="login"),
    path("logout/", login_views.logout_view, name="logout"),
    path("register/", login_views.register_view, name="register"),
    path("home/", main_views.home_view, name="home"),
    path("qrcodes/", include("qrcodes.urls")),
    path('admin/manageqr', qr_views.qr_code_generator, name='manage_qr'),
    path('admin/manageqr/<str:type>', qr_views.qr_code_generator, name='generate_qr'),
    path('admin/manageqr/<str:type>/<str:code>', qr_views.qr_code_generator, name='generate_qr'),
]