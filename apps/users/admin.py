from django.contrib import admin

from apps.users.models import *
# Register your models here.
admin.site.register([User, UserReward])