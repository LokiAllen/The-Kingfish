from django.shortcuts import render

from accounts.models import UserInfo

# Renders the home page
def home_view(request):
    return render(request, 'home.html')


def terms_and_conditions(request):
    return render(request, 'terms_and_conditions.html')