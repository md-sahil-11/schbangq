from rest_framework import serializers

from apps.users.models import User, UserReward


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "firstname",
            "lastname",
            "username",
            "is_active",
            "picture",
            "date_joined",
            "about"
        )
    

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