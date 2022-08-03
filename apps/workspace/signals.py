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