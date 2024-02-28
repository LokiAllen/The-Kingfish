# Static imports
from django.contrib.auth import login, logout
from django.contrib.auth.views import PasswordChangeView
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import View, FormView
from django.core.cache import cache

# Non-static imports
from .forms import *
from .models import UserInfo, UserFriends

"""
 * A custom view class that ensures the user is logged in for access
 * 
 * @author Jasper
"""
class NotLoggedInRequired(View):
    # Overrides the dispatch method to ensure the user is not logged in before proceeding with the view
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/home/')

        return super().dispatch(request, *args, **kwargs)

"""
 * A custom view class that ensures the user is not logged in for access
 * 
 * @author Jasper
"""
class LoggedInRequired(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        return redirect('/home/')

"""
 * A view class that presents the 'UserLogin' form and redirects to the
 * home page after the login is complete
 * 
 * @author Jasper
"""
class LoginView(NotLoggedInRequired, FormView):
    template_name = 'accounts/login.html'
    form_class = UserLogin

    # If the form is valid - logs them in
    def form_valid(self, form):
        login(self.request, form.user)
        return redirect('/home/')

"""
 * A view class that presents the 'RegisterForm' form and logs the user
 * in and redirects them to the home page after the register is complete
 * 
 * @author Jasper
"""
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

"""
 * A view class that presents the 'PasswordChangeView' to the user to securely change
 * their password, and redirects them to the home page after the change is complete
 * 
 * @author Jasper
"""
class ChangePasswordView(LoggedInRequired, PasswordChangeView):
    template_name = 'accounts/change.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        return redirect('/home/')

"""
 * A view class that logs the user out and redirects them to the home page
 * 
 * @author Jasper
"""
class LogoutView(LoggedInRequired, View):
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect('/home/')

"""
 * A view class that presents the user with a leaderboard to display the
 * information specified for the number or type of users specified
 * 
 * @author Jasper
"""
class LeaderboardView(LoggedInRequired, View):
    template_name = 'accounts/leaderboard.html'

    def dispatch(self, request, *args, **kwargs):
        leaderboard_type = self.request.GET.get('type', 'global')
        score_type = self.request.GET.get('score_type', 'coins')

        score_type = f'-{score_type}'

        if score_type not in ['-cumulativeScore', '-highscore', '-coins']:
            return redirect('/home/')

        data = self.get_leaderboard_data(leaderboard_type, score_type)

        return render(request, self.template_name, data)


    """
        Gets the dictionary leaderboard data values for the type and score_type specified
        
        @param leaderboard_type: The type of users to show (global, friends, ...)
        @param score_type: The type of score to show (coins, high score, ...) 
        @return A dictionary of users leaderboard data
    """
    def get_leaderboard_data(self, leaderboard_type, score_type):
        """
           Gets the current position of the user in the leaderboard with respect to the
           score_type specified in get_leaderboard_data()
           Caches the user's position for faster retrieval

           @param user: The user to get the position for
           @return Integer value of their current position in the leaderboard
        """
        def get_position(user):
            position_cache_key = f'user_{user.id}_position_{score_type}'
            position = cache.get(position_cache_key)

            if not position:
                match score_type:
                    case '-cumulativeScore':
                        position = UserInfo.objects.filter(cumulativeScore__gt=user.cumulativeScore).count() + 1
                    case '-highscore':
                        position = UserInfo.objects.filter(highscore__gt=user.highscore).count() + 1
                    case '-coins':
                        position = UserInfo.objects.filter(highscore__gt=user.coins).count() + 1

                cache.set(position_cache_key, position, timeout=300)

            return position

        """
            Gets the required user data for 'user' specified for the leaderboard
            
            @param user: The user whose data is being retrieved
            @return The required user data for the leaderboard 
        """
        def unpack_data(user):
            match score_type:
                case '-cumulativeScore':
                    value = user.cumulativeScore
                case '-highscore':
                    value = user.highscore
                case '-coins':
                    value = user.coins

            return {
                'username': user.user.username,
                'profile_picture': user.picture.url,
                'position': get_position(user),
                'value': value,
            }

        # Retrieves the base user's for the leaderboard and retrieves the required data for the leaderboard
        if leaderboard_type == 'friends':
            friend_objects = UserFriends.objects.filter(user_id=self.request.user.id)
            friend_ids = [friend.following_id for friend in friend_objects]

            friend_info_objects = UserInfo.objects.filter(user__in=friend_ids)
            top_friends_list = friend_info_objects.order_by(score_type)

            top_user_list = [unpack_data(user) for user in top_friends_list]

        else:
            top_users_object = UserInfo.objects.order_by(score_type)
            top_user_list = [unpack_data(user) for user in top_users_object]

        top_user_list.append(unpack_data(self.request.user.userinfo))

        return {'top_users': top_user_list}


"""
 * Standard class for handling functions related to the friends system
 *
 * @author Jasper
"""
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


"""
 * A custom view class that redirects the user to either their
 * own profile page, or the users profile page correspondingly
 * 
 * @author Jasper
"""
class ProfileDispatch(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.username == kwargs['username']:
                return OwnProfileView.as_view()(request, *args, **kwargs)
            return ProfileView.as_view()(request, *args, **kwargs)

        return redirect('/home/')

"""
 * A class based form for the own users profile to allow them
 * to edit their profile information
 *
 * @author Jasper
"""
class OwnProfileView(FormView):
    template_name = 'accounts/ownprofile.html'
    form_class = ChangeInfo

    # Sets the form context to that for the user
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    # Sets the initial values inside the form box to their current information
    def get_initial(self):
        initial = super().get_initial()
        initial['email'] = self.request.user.email
        initial['username'] = self.request.user.username
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        return initial

    # If the form is valid it will save the information specified
    def form_valid(self, form):
        user = self.request.user
        user.email = form.cleaned_data['email']
        user.username = form.cleaned_data['username']
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']

        # Deletes and updates the profile picture if it has changed
        if form.cleaned_data['profile_picture']:
            default_storage.delete(user.userinfo.picture.path)
            user.userinfo.picture = form.cleaned_data['profile_picture']
            user.userinfo.save()

        user.save()

        current_url = reverse('accounts:profile', kwargs={'username': user.username})

        return redirect(current_url)

"""
 * A class based view to display profile information on specific users
 *
 * @author Jasper
"""
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