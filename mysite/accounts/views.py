from django.contrib.auth import login, logout
from django.contrib.auth.views import PasswordChangeView
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import View, FormView
from django.core.cache import cache

import re

from .forms import *
from .models import UserInfo, UserFriends


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

        user_info.picture = form.cleaned_data['profile_picture']
        if not user_info.picture:
            user_info.picture = 'default.png'

        # Saves their account to the db and logs them in
        user.save()
        user_info.save()
        login(self.request, user)

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
# Adds all top users to the leaderboard data based on url parameter 'friends' otherwise is 'global'
# Currently caches the user position for 5 minutes as quite expensive operation to calculate position everytime leaderboard loaded
class LeaderboardView(LoggedInRequired, View):
    template_name = 'accounts/leaderboard.html'

    def dispatch(self, request, *args, **kwargs):
        score_type = self.request.GET.get('score_type', 'cumulative')
        #self.num_users = 15 # --> If adding limit to users uncomment this
        if score_type == 'cumulative':
            self.leaderboard_value = "-cumulativeScore"
        else:
            self.leaderboard_value = "-highscore"

        leaderboard_type = self.request.GET.get('type', 'global')


        data = self.get_leaderboard_data(leaderboard_type, score_type)

        return render(request, self.template_name, data)
    def get_leaderboard_data(self, type, score_type='cumulative'):
        def get_position(user, score_field):
            position_cache_key = f'user_{user.id}_position_{score_field}'
            position = cache.get(position_cache_key)

            if not position:
                if score_field == 'cumulativeScore':
                    position = UserInfo.objects.filter(cumulativeScore__gt=user.cumulativeScore).count() + 1
                else:
                    position = UserInfo.objects.filter(highscore__gt=user.highscore).count() + 1

                cache.set(position_cache_key, position, timeout=300)

            return position

        def unpack_data(user):
            return {
                'username': user.user.username,
                'profile_picture': user.picture.url,
                'position': get_position(user, 'cumulativeScore' if score_type == 'cumulative' else 'highscore'),
                'cumulativeScore': user.cumulativeScore,
                'highscore': user.highscore,}

        # Currently this is a list of anyone the user is following instead of 'friends'
        if type == 'friends':
            friend_objects = UserFriends.objects.filter(user_id=self.request.user.id)
            friend_ids = [friend.following_id for friend in friend_objects]

            friend_info_objects = UserInfo.objects.filter(user__in=friend_ids)
            top_friends_list = friend_info_objects.order_by(self.leaderboard_value) # [:self.num_users]  # --> If adding limit to users uncomment this

            top_user_list = [unpack_data(user) for user in top_friends_list]

        else:
            top_users_object = UserInfo.objects.order_by(self.leaderboard_value) # [:self.num_users]  # --> If adding limit to users uncomment this
            top_user_list = [unpack_data(user) for user in top_users_object]

        top_user_list.append(unpack_data(self.request.user.userinfo))

        return {'top_users': top_user_list}


class FriendSystem:
    def friend_query(request, *args, **kwargs):
        user = User.objects.filter(id=request.user.id)
        user_to_query = User.objects.filter(username=kwargs['user'])

        if user.exists() and user_to_query.exists():
            user, user_to_query = user.first(), user_to_query.first()
            friend_check__object = UserFriends.objects.filter(user_id=user_to_query.id, following_id=user.id)

            if friend_check__object.exists():
                friend = friend_check__object.first()
                friend.is_friend = kwargs['method'] == 'add'
                friend.save()

            if kwargs['method'] == 'add':
                return UserFriends.objects.create(user_id=user.id, following_id=user_to_query.id,
                                              is_friend=friend_check__object.exists())
            return UserFriends.objects.filter(user_id=user.id, following_id=user_to_query.id).delete()


# Redirects to either their own profile to edit, or the users profile
class ProfileDispatch(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:

            if request.user.username == kwargs['username']:
                return OwnProfileView.as_view()(request, *args, **kwargs)

            return ProfileView.as_view()(request, *args, **kwargs)

        return redirect('/home/')

# Own users profile (currently a FormView to edit their info)
class OwnProfileView(FormView):
    template_name = 'accounts/ownprofile.html'
    form_class = ChangeInfo

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial['email'] = self.request.user.email
        initial['username'] = self.request.user.username
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        return initial

    def form_valid(self, form):
        user = self.request.user
        user.email = form.cleaned_data['email']
        user.username = form.cleaned_data['username']
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']

        if form.cleaned_data['profile_picture']:
            default_storage.delete(user.userinfo.picture.path)
            user.userinfo.picture = form.cleaned_data['profile_picture']
            user.userinfo.save()

        user.save()

        current_url = reverse('accounts:profile', kwargs={'username': user.username})

        return redirect(current_url)

# Viewing users profiles
class ProfileView(View):
    def get(self, request, *args, **kwargs):
        if request.user.username == kwargs['username']:
            return OwnProfileView.as_view()(request, *args, **kwargs)

        user_data = User.objects.filter(username=kwargs['username'])
        if user_data:
            user_data = user_data.first()

            following = UserFriends.objects.filter(user_id=request.user.id, following_id=user_data.id)
            friend = False
            if following:
                friend = following.first().is_friend

            return render(request, 'accounts/profile.html', {'user_data': user_data, 'following': following, 'friend': friend})

    def post(self, request, *args, **kwargs):
        if FriendSystem.friend_query(request, **{'method':request.POST.get('method', None), 'user':kwargs['username']}):
            return HttpResponse(200)