import re
from django.utils import timezone
from django.shortcuts import get_object_or_404

from rest_framework.decorators import action
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from apps.workspace.api.serializers import WorkspaceSerializer

from apps.workspace.models import *

class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    permission_classes = [permissions.AllowAny,]

    # def create(self, request, *args, **kwargs):
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save(serializer)
        # return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        item = self.get_object()
        member = WorkspaceMember.objects.filter(workspace=item, user=request.user).first()
        
        if member.is_leader or member.is_manager:
            serializer = self.serializer_class(item, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(status=status.HTTP_401_UNAUTHORIZED)
