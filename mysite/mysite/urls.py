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
from mysite import settings, views
from accounts import views as account_views
from shop import views as shop_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('siteadmin/', include('siteadmin.urls')),
    path('accounts/', include('accounts.urls')),
    path('qrcodes/', include('qrcodes.urls')),
    path('game/', include('game.urls')),
    path("quiz/", include("quiz.urls")),
    path('api/', include('api.urls')),
    path('', views.home_view, name='home'),
    path('home/', views.home_view, name='home_view'),
    path('leaderboard/', account_views.LeaderboardView.as_view(), name='leaderboard'),
    path('shop/', shop_views.ShopView.as_view(), name='shop'),
    path('terms+and+conditions/', views.terms_and_conditions, name='terms_and_conditions')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)