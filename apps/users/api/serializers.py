from pyexpat import model
from rest_framework import serializers

from apps.users.models import User, UserReward


class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField(read_only=True)
    followings_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "firstname",
            "lastname",
            "username",
            "is_leader",
            "is_manager",
            "is_employee",
            "is_active",
            "picture",
            "date_joined",
            "about"
        )
    
    def get_followers_count(self, instance):
        return instance.followers.all().count()

    def get_followings_count(self, instance):
        return instance.followings.all().count()


class UserRewardSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserReward
        fields = (
            "id",
            "points",
            "user",
            "is_redeemed"
        )