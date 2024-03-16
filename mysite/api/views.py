# Static imports
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.core.cache import cache

# Non-static imports
from .models import UserMessage
from .serializers import MessageSerializer, ScoreSerializer, ShopSerializer, UserTitleSerializer, \
    UserBackgroundSerializer
from accounts.models import UserInfo, UserFriends, Titles, Backgrounds, UserOwnedTitles, UserOwnedBackgrounds
from shop.models import Shop

class MessageData(generics.GenericAPIView):
    """
     * Returns a list of all the messages sent and retrieved for a user and their friend
     *
     * @author Jasper
    """
    serializer_class = MessageSerializer

    # Gets the queryset used for the view, which is the messages sent and received between the users
    def get_queryset(self):
        receiver = User.objects.get(username__iexact=self.kwargs['username'])
        user = self.request.user
        return UserMessage.objects.filter(sender=user, receiver=receiver) | UserMessage.objects.filter(sender=receiver, receiver=user)

    # GET request is to get the message data
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)

    # POST request is used to send a message
    def post(self, request, *args, **kwargs):
        request.data.update({'sender': request.user.id, 'receiver': User.objects.get(username__iexact=kwargs['username']).id})
        serializer = self.get_serializer(data=request.data)

        # Checks if the message content is valid (I.E empty message will be false)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class LeaderboardData(ListAPIView):
    """
     * Returns a list of all users leaderboard values
     *
     * @author Jasper
    """
    serializer_class = ScoreSerializer

    def get_queryset(self):
        print(self.kwargs)
        score_type = self.kwargs.get('score_type', None)
        leaderboard_type = self.kwargs.get('leaderboard_type', None)

        if not leaderboard_type or not score_type:
            return Response({'error': 'Leaderboard type is not valid'}, status=status.HTTP_400_BAD_REQUEST)

        if leaderboard_type == 'friends':
            friend_objects = UserFriends.objects.filter(user_id=self.request.user.id)
            friend_ids = [friend.following_id for friend in friend_objects]

            friend_info_objects = UserInfo.objects.filter(user__in=friend_ids)
            top_user_list = friend_info_objects.order_by(f'-{score_type}')

        else:
            top_user_list = UserInfo.objects.order_by(f'-{score_type}')

        return list(top_user_list) + list(UserInfo.objects.filter(user=self.request.user))

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['score_type'] = self.kwargs.get('score_type')
        context['leaderboard_type'] = self.kwargs.get('leaderboard_type')
        return context
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ShopData(generics.GenericAPIView):
    """
     * Returns a list of all the current shop data excluding the users currently owned items
     *
     * @author Jasper
    """
    serializer_class = ShopSerializer

    def get_queryset(self):
        """
        Removes currently owned items from the list before returning the list of shop items
        """
        user_owned_titles = UserOwnedTitles.objects.filter(user=self.request.user)
        user_owned_title_ids = user_owned_titles.values_list('title_id', flat=True)
        title_objects = Shop.objects.filter(item_type_id=19)

        user_owned_backgrounds = UserOwnedBackgrounds.objects.filter(user=self.request.user)
        user_owned_background_ids = user_owned_backgrounds.values_list('background_id', flat=True)
        background_objects = Shop.objects.filter(item_type_id=23)

        return title_objects.exclude(item_id__in=user_owned_title_ids) | background_objects.exclude(item_id__in=user_owned_background_ids)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ShopSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if 'item' in request.data:
            item_id_type = request.data['item'].split('-')
            item_id, item_type = item_id_type[0], item_id_type[1]
            shop_object = Shop.objects.filter(item_id=item_id, item_type=item_type).first()

            if shop_object and request.user.userinfo.coins > shop_object.price:
                """ The way the shop model is setup, the category is that categories corresponding database ID.
                    If you want to add a new category, to find it go to localhost:8000/admin page and add a new
                    item to 'Shops' as its the easiest way. Otherwise title = 19, background = 23 """
                match item_type:
                    case '19':
                        queryset = {'user': request.user.id, 'title': shop_object.item_object.id}
                        serializer = UserTitleSerializer(data=queryset, many=False)
                    case '23':
                        queryset = {'user': request.user.id, 'background': shop_object.item_object.id}
                        serializer = UserBackgroundSerializer(data=queryset, many=False)

                if serializer.is_valid():
                    request.user.userinfo.coins -= shop_object.price
                    request.user.userinfo.save()
                    serializer.save()

                    return Response({'coins': request.user.userinfo.coins}, status=200)

        return Response({}, status=400)
