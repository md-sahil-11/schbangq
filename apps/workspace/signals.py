from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from apps.workspace.helpers import invite_mail
from apps.workspace.models import *

@receiver(post_save, sender=Workspace)
def creator_to_leader(sender, instance, created, **kwargs):
    if created:
        WorkspaceMember.objects.create(
            user=instance.creator,
            workspace=instance,
            is_leader=True
        )

@receiver(post_save, sender=Invitation)
def send_invite_mail(sender, instance, created, **kwargs):
    url = (
        f"{settings.HOST_URL}/api/workspaces/{instance.workspace.slug}/join?invitation_id={instance.id}",
    )
    invite_mail(
        instance.email, url, instance.invited_by
    )

@receiver(post_save, sender=Task)
def notify_task_handler(sender, instance, created, **kwargs):
    if created:
        Notification.objects.get_or_create(
            user=instance.assignee,
            text=f"You have been assigned a task with title '{instance.title}' by {instance.assignor}",
            workspace=instance.project.workspace
        )
    elif not instance.is_pending:
        Notification.objects.get_or_create(
            user=instance.assignor,
            text=f"Task with title '{instance.title}' has been submitted by {instance.assignee}",
            workspace=instance.project.workspace
        )