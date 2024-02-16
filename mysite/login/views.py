from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import NewAuthenticationForm, NewUserCreationForm

# Login page
def login_view(request):
    # Doesn't let a logged-in user go to login page, easily changed to something like a logout page
    if request.user.is_authenticated:
        return redirect('/home/')

    # If the user is sending a POST request (submitting a login) it verifies their credentials and redirects based on it
    if request.method == 'POST':
        login_form = NewAuthenticationForm(request, data=request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/home/')
            else:
                messages.error(request, 'Invalid username or password')

    else:
        login_form = NewAuthenticationForm()

    return render(request, 'login.html', {'form': login_form})

# Register page - Basically the same as login but for the form 'NewUserCreationForm'
def register_view(request):
    if request.user.is_authenticated:
        return redirect('/home/')

    if request.method == 'POST':
        register_form = NewUserCreationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            login(request, user)

            return redirect('home')
    else:
        register_form = NewUserCreationForm()

    return render(request, 'register.html', {'form': register_form})

# Logs a user out and sends them to the home page
def logout_view(request):
    logout(request)
    return redirect('/home/')

