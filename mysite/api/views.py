# Static imports
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.db.models import Case, Value, When, BooleanField, Q

# Non-static imports
from .models import UserMessage
from .serializers import MessageSerializer, ScoreSerializer, ShopSerializer, UserTitleSerializer, \
    UserBackgroundSerializer, UserInfoSerializer
from accounts.models import UserInfo, UserFriends, Titles, Backgrounds, UserOwnedTitles, UserOwnedBackgrounds
from shop.models import Shop

class SuperUserCheck(IsAdminUser):
    """
     * Checks whether a user is a super user to access the endpoint
     *
     * @author Jasper
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class GameKeeperCheck(IsAdminUser):
    """
     * Checks whether a user is a super user to access the endpoint
     *
     * @author Jasper
    """
    def has_permission(self, request, view):
        return request.user and (request.user.is_staff or request.user.is_superuser)

class MessageData(generics.GenericAPIView):
    """
     * Returns a list of all the messages sent and retrieved for a user and their friend
     * Post requests will send a message from the user to the user being messaged
     *
     * @author Jasper
    """
    permission_classes = [IsAuthenticated]
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
     * Post requests are not accepted
     *
     * @author Jasper
    """
    permission_classes = [IsAuthenticated]
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
     * Post requests will purchase the specified item id and type for the user sending the request
     *
     * @author Jasper
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ShopSerializer

    def get_queryset(self):
        """
        Sets the 'owned' flag for each item whether the user owns it as otherwise cannot be found.
        """
        user = self.request.user

        # Get a list of owned title and backgrounds
        owned_title_ids = UserOwnedTitles.objects.filter(user=user).values_list('title_id', flat=True)
        owned_background_ids = UserOwnedBackgrounds.objects.filter(user=user).values_list('background_id', flat=True)

        # Annotate the Shop queryset with an 'owned' flag relative to whether the user owns it
        shop_items = Shop.objects.annotate(
            owned=Case(
                When(Q(item_id__in=owned_title_ids) & Q(item_type_id=19), then=Value(True)),
                When(Q(item_id__in=owned_background_ids) & Q(item_type_id=23), then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            )
        )

        return shop_items

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ShopSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if 'item' in request.data and request.data['item']:
            item_id_type = request.data['item'].split('-')

            try:
                item_id, item_type = item_id_type[0], item_id_type[1]
            except IndexError:
                return Response({'error': 'Invalid item'}, status=status.HTTP_400_BAD_REQUEST)

            shop_object = Shop.objects.filter(item_id=item_id, item_type=item_type).first()

            if shop_object and request.user.userinfo.coins > shop_object.price:
                """ The way the shop model is setup, the category is that categories corresponding database ID.
                    If you want to add a new category, to find it go to localhost:8000/admin page and add a new
                    item to 'Shops' as its the easiest way. Otherwise title = 19, background = 23 """
                match item_type:
                    case '19':
                        queryset = {'user': request.user.id, 'title': shop_object.item_id}
                        serializer = UserTitleSerializer(data=queryset, many=False)
                    case '23':
                        queryset = {'user': request.user.id, 'background': shop_object.item_id}
                        serializer = UserBackgroundSerializer(data=queryset, many=False)

                if serializer.is_valid():
                    request.user.userinfo.coins -= shop_object.price
                    request.user.userinfo.save()
                    serializer.save()

                    return Response({'coins': request.user.userinfo.coins}, status=200)

        return Response({}, status=400)


class UserData(generics.GenericAPIView):
    """
     * Returns a list of a users username, coins, highscore and cumulativeScore
     * Post requests will update the values inside the request body
     *
     * @author Jasper
    """
    permission_classes = [SuperUserCheck]
    serializer_class = UserInfoSerializer
    def get(self, request, *args, **kwargs):
        user_object = User.objects.filter(username__iexact=kwargs['username']).first()
        if user_object:
            queryset = UserInfo.objects.get(user=user_object)
            serializer = UserInfoSerializer(queryset, many=False)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_404_NOT_FOUND)
    def post(self, request, *args, **kwargs):
        user_object = User.objects.filter(username__iexact=kwargs['username']).first()

        if not user_object:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        user_info_object = UserInfo.objects.get(user=user_object)
        serializer = self.get_serializer(user_info_object, data=request.data, partial=True)

        if serializer.is_valid():
            user_object.is_staff = request.data.get('is_staff', request.user.is_staff)
            user_object.is_superuser = request.data.get('is_superuser', request.user.is_superuser)

            serializer.save()
            user_object.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminShopData(generics.GenericAPIView):
    """
     * Returns a list of all the current shop data
     * Post requests will update the shop items price, description and cost for each one that is in the request body
     *
     * @author Jasper
    """
    permission_classes = [GameKeeperCheck]
    serializer_class = ShopSerializer

    def get_queryset(self):
        return Shop.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ShopSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if kwargs['item_type_id']:
            item_id_type = kwargs['item_type_id'].split('-')

            name = request.data.get('name', None)
            description = request.data.get('description', None)
            price = request.data.get('price', None)

            try:
                item_id, item_type = item_id_type[0], item_id_type[1]
            except IndexError:
                return Response({'error': 'Invalid item'}, status=status.HTTP_400_BAD_REQUEST)

            shop_object = Shop.objects.filter(item_id=item_id, item_type=item_type).first()
            if name:
                shop_object.name = name
            if description:
                shop_object.description = description
            if price:
                shop_object.price = price

            shop_object.save()

            return Response({}, status=200)

        return Response({}, status=400)