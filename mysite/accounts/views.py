from django.contrib.auth import login, logout
from django.contrib.auth.views import PasswordChangeView
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View, FormView
from django.core.cache import cache

from .forms import *
from .models import UserInfo


# Used for views that require the user to not be logged in
class NotLoggedInRequired(View):
    # Overrides the dispatch method to ensure the user is not logged in before proceeding with the view
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/home/')

        return super().dispatch(request, *args, **kwargs)

# Used for views that require the user to be logged in
class LoggedInRequired(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        return redirect('/home/')

# Login view
class LoginView(NotLoggedInRequired, FormView):
    template_name = 'accounts/login.html'
    form_class = UserLogin

    # If the form is valid - logs them in
    def form_valid(self, form):
        login(self.request, form.user)
        return redirect('/home/')

# Register view
class RegisterView(NotLoggedInRequired, FormView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save(commit=False)

        # Create a UserInfo entry for the user
        user_info = UserInfo()
        user_info.user = user

        # Saves their account to the db and logs them in
        user.save()
        user_info.save()
        login(self.request, user)

        return redirect('/home/')

# Change Email (all types of changes are basically the same format)
class ChangeEmailView(LoggedInRequired, FormView):
    template_name = 'accounts/change.html'
    form_class = ChangeEmail

    # Tells the form the 'User' that is changing their email
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    # Sets the initial contents of the form to the user's email
    def get_initial(self):
        initial = super().get_initial()
        initial['email'] = self.request.user.email
        return initial

    def form_valid(self, form):
        user = self.request.user
        user.email = form.cleaned_data['email']
        user.save()

        return redirect('/home/')

# Change Username
class ChangeUsernameView(LoggedInRequired, FormView):
    template_name = 'accounts/change.html'
    form_class = ChangeUsername

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial['username'] = self.request.user.username
        return initial

    def form_valid(self, form):
        user = self.request.user
        user.username = form.cleaned_data['username']
        user.save()

        return redirect('/home/')

# Change Info (currently first name and last name - depending on what is used for accounts further it can be altered for them
class ChangeInfoView(LoggedInRequired, FormView):
    template_name = 'accounts/change.html'
    form_class = ChangeInfo

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        return initial

    def form_valid(self, form):
        user = self.request.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()

        return redirect('/home/')

# Change Password (handled by PasswordChangeView)
class ChangePasswordView(LoggedInRequired, PasswordChangeView):
    template_name = 'accounts/change.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        return redirect('/home/')

# Logout
class LogoutView(LoggedInRequired, View):
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect('/home/')

# Leaderboard view
class LeaderboardView(LoggedInRequired, View):
    def dispatch(self, request, *args, **kwargs):
        # Loads the page if it hasn't been loaded
        page_loaded = request.GET.get('page_loaded', False)
        if not page_loaded:
            return render(request, 'accounts/leaderboard.html')

        # Get number of users to show (default 3)
        self.num_users = request.GET.get('num_users', None)
        if not self.num_users:
            self.num_users = 3

        # GET request sends as a string -> Convert to integer
        self.num_users = int(self.num_users)

        # Get the values for a 'coins' leaderboard
        self.leaderboard_value = '-coins'
        data = self.get_leaderboard_data()

        return JsonResponse(data)

    # Get info for the users to show + the user
    def get_leaderboard_data(self):
        top_n_users_object = UserInfo.objects.order_by(self.leaderboard_value)[:self.num_users]

        # Adds all top users to the leaderboard data
        top_n_user_list = []
        for user in top_n_users_object:
            # Currently caches the user position for 5 minutes as quite expensive operation to calculate position every time leaderboard loaded
            position = cache.get(f'user_{user.id}_position')
            if not position:
                position = UserInfo.objects.filter(coins__gt=user.coins).count() + 1
                cache.set(f'user_{user.id}_position', position, timeout=300)

            top_n_user_list.append({'username': user.user.username, 'coins': user.coins, 'position': position})

        # Adds the user themselves to the end of the list (regardless of if they are already in the leaderboard data)
        user_object = UserInfo.objects.get(user=self.request.user)
        position = cache.get(f'user_{user.id}_position')
        if not position:
            position = UserInfo.objects.filter(coins__gt=user_object.coins).count() + 1
            cache.set(f'user_{user.id}_position', position, timeout=300)

        top_n_user_list.append({'username': self.request.user.username, 'coins': user_object.coins, 'position': position})

        return {'top_n_users': top_n_user_list}
