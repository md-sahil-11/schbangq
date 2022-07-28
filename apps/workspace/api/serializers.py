from rest_framework import serializers

from apps.workspace.models import *


class WorkspaceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Workspace
        fields = ("id", "title", "creator", "created_at", "slug",)
        read_only_fields = ("slug", "created_at",)