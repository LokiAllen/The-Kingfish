from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserMessage
from accounts.models import UserInfo

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.SerializerMethodField()

    def get_sender_username(self, obj):
        return obj.sender.username

    class Meta:
        model = UserMessage
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'sender_username']


class UserInfoSerializer(serializers.ModelSerializer):
    user_username = serializers.SerializerMethodField()

    def get_user_username(self, obj):
        return obj.user.username
    class Meta:
        model = UserInfo
        fields = ['id', 'user_username', 'coins', 'highscore', 'cumulativeScore']