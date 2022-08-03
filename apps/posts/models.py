from django.db import models

from apps.users.models import User


class Post(models.Model):
    title = models.CharField(max_length=240, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    poll_question = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="posts/image", null=True, blank=True)
    is_pinned = models.BooleanField(default=False)


class PollOption(models.Model):
    post = models.ForeignKey(Post, related_name="options", on_delete=models.CASCADE)
    text = models.CharField(max_length=240)
    vote = models.IntegerField(default=0)


class PostTag(models.Model):
    tag_choices = (
        ("TAG1", "tag1"),
        ("TAG2", "tag2"),
    )
    post = models.ForeignKey(Post, related_name='tags', on_delete=models.CASCADE)
    tag = models.CharField(max_length=120, choices=tag_choices, default="TAG1")


class PostLike(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)


class PostComment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    text = models.TextField()
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    