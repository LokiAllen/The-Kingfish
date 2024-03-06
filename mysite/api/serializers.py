from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserMessage
class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.SerializerMethodField()

    def get_sender_username(self, obj):
        return obj.sender.username

    class Meta:
        model = UserMessage
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'sender_username']