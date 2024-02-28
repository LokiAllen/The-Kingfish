from django.shortcuts import render

from accounts.models import UserInfo

# Renders the home page
def home_view(request):
    return render(request, 'home.html')