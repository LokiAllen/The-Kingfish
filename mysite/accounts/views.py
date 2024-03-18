# Static imports
from django.contrib.auth import login, logout
from django.contrib.auth.views import PasswordChangeView
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import View, FormView, TemplateView

# Non-static imports
from .forms import *
from .models import UserInfo, UserFriends, UserOwnedBackgrounds, UserOwnedTitles, Backgrounds, Titles

class NotLoggedInRequired(View):
    """
     * A custom view class that ensures the user is logged in for access
     *
     * @author Jasper
    """
    # Overrides the dispatch method to ensure the user is not logged in before proceeding with the view
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')

        return super().dispatch(request, *args, **kwargs)

class LoggedInRequired(View):
    """
     * A custom view class that ensures the user is not logged in for access
     *
     * @author Jasper
    """
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        return redirect('/')

class LoginView(NotLoggedInRequired, FormView):
    """
     * A view class that presents the 'UserLogin' form and redirects to the
     * home page after the login is complete
     *
     * @author Jasper
    """
    template_name = 'accounts/login.html'
    form_class = UserLogin

    # If the form is valid - logs them in
    def form_valid(self, form):
        login(self.request, form.user)
        return redirect('/')

class RegisterView(NotLoggedInRequired, FormView):
    """
     * A view class that presents the 'RegisterForm' form and logs the user
     * in and redirects them to the home page after the register is complete
     *
     * @author Jasper
    """
    template_name = 'accounts/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save(commit=False)

        # Create a UserInfo entry for the user
        user_info = UserInfo()
        user_info.user = user

        user_info.picture = form.cleaned_data['profile_picture']
        if not user_info.picture:
            user_info.picture = 'media/default.png'

        # Saves their account to the db and logs them in
        user.save()
        user_info.save()
        UserOwnedTitles.objects.create(user=user, title=Titles.objects.filter(title_name='Eco Rookie').first())
        UserOwnedBackgrounds.objects.create(user=user, background=Backgrounds.objects.filter(background_name='Default').first())
        login(self.request, user)

        return redirect('/')

class ChangePasswordView(LoggedInRequired, PasswordChangeView):
    """
     * A view class that presents the 'PasswordChangeView' to the user to securely change
     * their password, and redirects them to the home page after the change is complete
     *
     * @author Jasper
    """
    template_name = 'accounts/change.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        return redirect('/')

class LogoutView(LoggedInRequired, View):
    """
     * A view class that logs the user out and redirects them to the home page
     *
     * @author Jasper
    """
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect('/')

class FriendSystem:
    """
     * Standard class for handling functions related to the friends system
     *
     * @author Jasper
    """
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


class ProfileDispatch(View):
    """
     * A custom view class that redirects the user to either their
     * own profile page, or the users profile page correspondingly
     *
     * @author Jasper
    """
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.username == kwargs['username']:
                return OwnProfileView.as_view()(request, *args, **kwargs)
            return ProfileView.as_view()(request, *args, **kwargs)

        return redirect('/')

class OwnProfileView(FormView):
    """
     * A class based form for the own users profile to allow them
     * to edit their profile information
     *
     * @author Jasper
    """
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
        initial['title'] = self.request.user.userinfo.title_id
        initial['background'] = self.request.user.userinfo.background_id
        return initial

    # If the form is valid it will save the information specified
    def form_valid(self, form):
        user = self.request.user
        user.email = form.cleaned_data['email']
        user.username = form.cleaned_data['username']
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.userinfo.title = form.cleaned_data['title']
        user.userinfo.background = form.cleaned_data['background']

        print(user.email, user.username, user.first_name, user.last_name, user.userinfo.title, user.userinfo.background)

        # Deletes and updates the profile picture if it has changed
        if form.cleaned_data['profile_picture']:
            default_storage.delete(user.userinfo.picture.path)
            user.userinfo.picture = form.cleaned_data['profile_picture']
            user.userinfo.save()

        user.save()
        user.userinfo.save()

        current_url = reverse('accounts:profile', kwargs={'username': user.username})

        return redirect(current_url)

class ProfileView(View):
    """
     * A class based view to display profile information on specific users
     *
     * @author Jasper
    """
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

            return render(request, 'accounts/profile.html', {'user_data': user_data, 'following': following, 'friend': friend, 'title': user_data.userinfo.title.title_name})

    def post(self, request, *args, **kwargs):
        if FriendSystem.friend_query(request, **{'method':request.POST.get('method', None), 'user':kwargs['username']}):
            return HttpResponse(200)


class MessageUserChecks(LoggedInRequired, View):
    """
     * A custom view class that checks the user is logged in, messaging
     * an existing user, and is friends with them before access
     *
     * @author Jasper
    """
    def dispatch(self, request, *args, **kwargs):
        receiver = User.objects.filter(username__iexact=kwargs['username'])
        if receiver:
            user_friend_object = UserFriends.objects.filter(user_id=request.user.id, following_id=receiver[0].id)
            if user_friend_object.exists() and user_friend_object.first().is_friend:
                return super().dispatch(request, *args, **kwargs)
        return redirect('/')

class MessageView(MessageUserChecks, TemplateView):
    """
     * A view that presents the message form to the user, where the data for that is retrieved
     * via the endpoint inside the 'api' app
     *
     * @author Jasper
    """
    template_name = 'accounts/messages.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.kwargs['username']
        context['user_messaging'] = User.objects.filter(username__iexact=kwargs['username']).first()
        return context



class LeaderboardView(LoggedInRequired, View):
    """
     * A view that presents the leaderboard to the user, where the data for that is retrieved
     * via the endpoint inside the 'api' app
     *
     * @author Jasper
    """
    template_name = 'accounts/leaderboard.html'

    def dispatch(self, request, *args, **kwargs):
        return render(request, self.template_name)