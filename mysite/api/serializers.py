from rest_framework import serializers
from django.core.cache import cache

from .models import UserMessage
from accounts.models import UserInfo, UserOwnedTitles, UserOwnedBackgrounds
from shop.models import Shop

class MessageSerializer(serializers.ModelSerializer):
    """
     * An endpoint to serialize all message data between two users relative to the current user
     *
     * @author Jasper
    """
    sender_username = serializers.SerializerMethodField()

    def get_sender_username(self, obj):
        return obj.sender.username

    class Meta:
        model = UserMessage
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'sender_username']



class ScoreSerializer(serializers.ModelSerializer):
    """
     * An endpoint to serialize an individual users score relative to the type required
     * Used within the leaderboard to obtain all users scores
     *
     * @author Jasper
    """
    user_username = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()
    title_name = serializers.SerializerMethodField()

    def get_user_username(self, obj):
        return obj.user.username

    def get_value(self, obj):
        score_type = self.context.get('score_type', None)
        match score_type:
            case 'cumulativeScore':
                return obj.cumulativeScore
            case 'highscore':
                return obj.highscore
            case 'coins':
                return obj.coins
            case _:
                return -1

    def get_position(self, obj):
        score_type = self.context.get('score_type', None)
        position_cache_key = f'user_{obj.user.id}_{score_type}_position'
        position = cache.get(position_cache_key)

        if not position:
            match score_type:
                case 'cumulativeScore':
                    position = UserInfo.objects.filter(cumulativeScore__gt=obj.cumulativeScore).count() + 1
                case 'highscore':
                    position = UserInfo.objects.filter(highscore__gt=obj.highscore).count() + 1
                case 'coins':
                    position = UserInfo.objects.filter(coins__gt=obj.coins).count() + 1
                case _:
                    position = -1

            cache.set(position_cache_key, position, timeout=300)

        return position

    def get_title_name(self, obj):
        return obj.title.title_name

    class Meta:
        model = UserInfo
        fields = ['id', 'user_username', 'value', 'picture', 'title_name', 'position']

class ShopSerializer(serializers.ModelSerializer):
    """
     * An endpoint to serialize the current shop data
     *
     * @author Jasper
    """
    class Meta:
        model = Shop
        fields = ['name', 'description', 'price', 'item_id', 'item_type']

class UserTitleSerializer(serializers.ModelSerializer):
    """
     * An endpoint to serialize all the users owned titles
     *
     * @author Jasper
    """
    class Meta:
        model = UserOwnedTitles
        fields = ['user', 'title']

class UserBackgroundSerializer(serializers.ModelSerializer):
    """
     * An endpoint to serialize all the users owned backgrounds
     *
     * @author Jasper
    """
    class Meta:
        model = UserOwnedBackgrounds
        fields = ['user', 'background']
