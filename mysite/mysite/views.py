from django.shortcuts import render

# Anything related to the home page - Currently just renders separate functions based on their login status/account
def home_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == True:
            return render(request, 'home.html', {'logged_in': True, 'super': True})
        else:
            return render(request, 'home.html', {'logged_in': True, 'super': False})
    else:
        return render(request, 'home.html', {'logged_in': False})