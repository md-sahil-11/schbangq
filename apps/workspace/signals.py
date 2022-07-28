from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.workspace.models import *

@receiver(post_save, sender=Workspace)
def creator_to_leader(sender, instance, created, **kwargs):
    if created:
        WorkspaceMember.objects.create(
            user=instance.creator,
            workspace=instance,
            is_leader=True
        )