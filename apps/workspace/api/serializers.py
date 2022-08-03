from rest_framework import serializers
from apps.users.api.serializers import UserSerializer

from apps.workspace.models import *


class WorkspaceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Workspace
        fields = "__all__"
        read_only_fields = ("slug", "created_at",)


class WorkspaceMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkspaceMember
        fields = ("id", "user", "workspace", "is_leader", "is_manager", "is_employee",)

    
class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = "__all__"


class CaseStudySerializer(serializers.ModelSerializer):

    class Meta:
        model = CaseStudy
        fields = '__all__'
    

class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    assignor_id = serializers.PrimaryKeyRelatedField(
        source="user",
        queryset=User.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    ) 
    assignor = UserSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(
        source="user",
        queryset=User.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    ) 
    assignee = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ("title", "assignor", "assignor_id", "assignee", "assignee_id", "assigned_at", "deadline_at", "priority", "progress", "reward", "is_pending", "project")


class TaskCommentSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        source="user",
        queryset=User.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = TaskComment
        fields = ("id", "user", "task", "internal_chat", "user_id", "text")