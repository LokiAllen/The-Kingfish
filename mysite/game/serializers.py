from rest_framework import serializers
from accounts.models import UserInfo

class UserInfoSerializer(serializers.ModelSerializer):
    user_username = serializers.SerializerMethodField()

    def get_user_username(self, obj):
        return obj.user.username

    class Meta:
        model = UserInfo
        fields = ['id', 'user_username', 'coins', 'highscore', 'cumulativeScore']