from rest_framework import serializers

from apps.posts.models import *
from apps.users.models import *
from apps.users.api.serializers import *


class PollOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PollOption
        fields = ("id", "text", "post", "vote")


class PostTagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PostTag
        fields = ("id", "tag", "post")


class PostSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        source="user",
        queryset=User.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )
    user = UserSerializer(read_only=True)

    options = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id", "title", "body", "image", "poll_question", "user", "user_id", "options", "tags", "is_pinned", "likes_count", "comments_count"
        )

    def get_options(self, instance):
        options = PollOption.objects.filter(post=instance)
        return PollOptionSerializer(options, many=True).data

    def get_tags(self, instance):
        tags = PostTag.objects.filter(post=instance)
        return PostTagSerializer(tags, many=True).data
    
    def get_likes_count(self, instance):
        return instance.likes.all().count()
    
    def get_comments_count(self, instance):
        return instance.comments.all().count()


class PostCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        source="user",
        queryset=User.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )
 
    class Meta:
        model = PostComment
        fields = ("id", "post", "text", "user_id", "user")
    