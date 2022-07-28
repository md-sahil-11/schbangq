from django.db import models
from apps.users.models import User
from django.utils import timezone
from django.utils.text import slugify


class Workspace(models.Model):
    title = models.CharField(max_length=240)
    creator = models.ForeignKey(
        User, related_name='created_workspaces', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(default=timezone.now)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Workspace, self).save(*args, **kwargs)


class WorkspaceMember(models.Model):
    user = models.ForeignKey(User, related_name='workspaces', on_delete=models.CASCADE)
    workspace = models.ForeignKey(
        Workspace, related_name='members', on_delete=models.CASCADE
    )
    is_leader = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'workspace',)


class Invitation(models.Model):
    role_choices = (
        ('EMPLOYEE', 'employee'),
        ('MANAGER', 'manager'),
        ('LEADER', 'leader'),
    )
    workspace = models.ForeignKey(Workspace, related_name='invitations', on_delete=models.CASCADE)
    email = models.EmailField()
    invited_by = models.ForeignKey(User, related_name='invites', on_delete=models.SET_NULL, null=True)
    invited_at = models.DateTimeField(default=timezone.now)
    role = models.CharField(choices=role_choices, default='EMPLOYEE', max_length=100)