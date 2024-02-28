from django.shortcuts import render

from accounts.models import UserInfo

# Anything related to the home page - Currently just renders separate functions based on their login status/account
def home_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == True:
            return render(request, 'home.html')
        else:
            return render(request, 'home.html')
    else:
        return render(request, 'home.html')