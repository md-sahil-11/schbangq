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

    class Meta:
        model = Task
        fields = '__all__'


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
        fields = ("id", "user", "internal_chat", "user_id")