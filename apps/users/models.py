from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from apps.users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, db_index=True)
    firstname = models.CharField(max_length=100, null=True, blank=True)
    lastname = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(
        max_length=100, unique=True, db_index=True, blank=True, null=True
    )
    is_leader = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, db_index=True)
    date_joined = models.DateTimeField(default=timezone.now)
    picture = models.ImageField(upload_to="users/profile", null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    
    objects = UserManager()

    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.email

    @property
    def fullname(self):
        fullname = "%s %s" % (self.firstname, self.lastname)
        return fullname.strip()


class Follow(models.Model):
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='followings', on_delete=models.CASCADE)


# create on completion of task
class UserReward(models.Model):
    points = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(User, related_name="rewards", on_delete=models.CASCADE, null=True, blank=True)
    is_redeemed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-id",]


