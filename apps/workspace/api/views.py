import re
from django.utils import timezone
from django.conf import settings
from django.shortcuts import get_object_or_404
from apps.users.api.serializers import UserSerializer
from apps.users.models import UserReward
from apps.workspace.helpers import invite_mail
from django.contrib.auth import authenticate

from rest_framework.decorators import action
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from apps.workspace.api.serializers import *

from apps.workspace.models import *

class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    permission_classes = [permissions.IsAuthenticated,]

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
    
    @action(
        detail=False,
        methods=["GET"],
        permission_classes=(permissions.AllowAny,)
    )
    def all(self, request, *args, **kwargs):
        serializer = self.serializer_class(Workspace.objects.all(), many=True)
        return Response({'results': serializer.data})
    
    @action(
        detail=True,
        methods=["GET"],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_user_type(self, request, *args, **kwargs):
        ws = self.get_object()
        member = WorkspaceMember.objects.filter(workspace=ws, user_id=request.user.id).first()
        if member.is_leader:
            return Response({'user_type': 'leader'})
        elif member.is_manager:
            return Response({'user_type': 'manager'})
        elif member.is_employee:
            return Response({'user_type': 'employee'})
        return Response({'user_type': 'client'})

    @action(
        detail=True,
        methods=["GET"],
        permission_classes=(permissions.IsAuthenticated,),
        serializer_class=(WorkspaceMemberSerializer)
    )
    def members(self, request, *args, **kwargs):
        ws = self.get_object()
        return Response({
            'results': self.serializer_class(ws.members.all(), many=True).data
        })
    
    @action(
        detail=True,
        methods=["POST"],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def invite(self, request, *args, **kwargs):
        ws = self.get_object()
        email = request.data.get('email')
        role = request.data.get('role')
        instance, _ = Invitation.objects.get_or_create(
            email=email,
            workspace=ws,
            role=role,
            invited_by=request.user
        )
        login_url = f"{settings.HOST_URL}/api/workspaces/{instance.workspace.slug}/join?invitation_id={instance.id}"
        invite_mail(
            instance.email, login_url, instance.invited_by
        )

        return Response({'success': True})

    @action(
        detail=True,
        methods=["POST"],
        lookup_field = 'slug',
        permission_classes=(permissions.IsAuthenticated,),
    )
    def join(self, request, *args, **kwargs):
        ws = self.get_object()
        invite_id = self.request.query_params.get('invitation_id')
        invitation = get_object_or_404(Invitation, id=invite_id)
        password = request.data.get("password")
        firstname = request.data.get("firstname")
        lastname = request.data.get("lastname")
        username = request.data.get("username")

        if User.objects.filter(email=invitation.email).exists():
            user = authenticate(email=invitation.email, password=password)
        else:
            user = User.objects.create(
                email=invitation.email,
                firstname=firstname,
                lastname=lastname,
                username=username
            )
            user.set_password(password)
            user.save()
        if user is not None:
            wm, _ = WorkspaceMember.objects.get_or_create(
                user=user,
                workspace=ws
            )
            if invitation.role == 'manager':
                wm.is_manager = True
            elif invitation.role == 'leader':
                wm.is_leader = True
            else:
                wm.is_employee = True
            wm.save()
        if not user:
            return Response({"success": False, "err": "Something went wrong!!!"})
        
        return Response({'success': True, "data": UserSerializer(user).data})

    @action(
        detail=True,
        methods=['GET'],
        permission_classes=(permissions.AllowAny,)
    )
    def services(self, request, *args, **kwargs):
        workspace = self.get_object()
        queryset = workspace.services.all()
        serializer = ServiceSerializer(queryset, many=True)
        return Response({'count': queryset.count(), 'results': serializer.data})
    
    @action(
        detail=True,
        methods=['GET'],
        permission_classes=(permissions.AllowAny,)
    )
    def case_studies(self, request, *args, **kwargs):
        workspace = self.get_object()
        queryset = workspace.case_studies.all()
        serializer = CaseStudySerializer(queryset, many=True)
        return Response({'count': queryset.count(), 'results': serializer.data})
    
    @action(
        detail=True,
        methods=['GET'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def transactions(self, request, *args, **kwargs):
        workspace = self.get_object()
        member = WorkspaceMember.objects.filter(
            user=request.user, workspace=workspace
        ).first()
        queryset = Transaction.objects.filter(
            user=request.user, workspace=workspace
        )
        if member.is_leader or member.is_manager:
            queryset = Transaction.objects.filter(workspace=workspace)

        serializer = TransactionSerializer(queryset, many=True)
        return Response({'count': queryset.count(), 'results': serializer.data})
    
    @action(
        detail=True,
        methods=['GET'],
        permission_classes=(permissions.AllowAny,)
    )
    def projects(self, request, *args, **kwargs):
        workspace = self.get_object()
        member = WorkspaceMember.objects.filter(
            user=request.user, workspace=workspace
        ).first()
        queryset = Project.objects.filter(
            user=request.user, workspace=workspace
        )
        if member.is_leader or member.is_manager:
            queryset = Project.objects.filter(workspace=workspace)

        serializer = ProjectSerializer(queryset, many=True)
        return Response({'count': queryset.count(), 'results': serializer.data})
    
    @action(
        detail=True,
        methods=['GET'],
    )
    def all_tasks(self, request, *args, **kwargs):
        workspace = self.get_object()
        is_pending = request.query_params.get('is_pending', None)
        queryset = Task.objects.filter(
            project__workspace=workspace
        )
        if is_pending is not None:
            if is_pending == "false":
                queryset = queryset.filter(is_pending=False)
            else:
                queryset = queryset.filter(is_pending=True)
        author_type = request.query_params.get('author_type', None)
        if author_type is not None:
            if author_type == "manager":
                queryset = queryset.filter(
                    assignor=request.user
                )
            elif author_type == "employee":
                queryset = queryset.filter(assignee=request.user)
            
            serializer = TaskSerializer(queryset, many=True)
            return Response({'count': queryset.count(), 'results': serializer.data})
        return Response({'count': 0, 'results': []})

    @action(
        detail=True,
        methods=['GET'],
    )
    def project_tasks(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=int(self.kwargs.get('pk')))
        queryset = project.tasks.all()
        serializer = TaskSerializer(queryset, many=True)
        return Response({'count': queryset.count(), 'results': serializer.data})

    @action(
        detail=True,
        methods=['PUT'],
        serializer_class=TaskSerializer
    )
    def complete_task(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=int(self.kwargs.get('pk')))
        if request.user == task.assignee:
            task.is_pending = False
            task.save()
            UserReward.objects.get_or_create(
                user=request.user, points=task.reward
            )
            return Response({"success": True})
        return Response({"success": False})
    
    @action(
        detail=True,
        methods=['PUT'],
        serializer_class=ProjectSerializer
    )
    def complete_project(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=int(self.kwargs.get('pk')))
        project.is_pending = False
        project.save()
        return Response({"success": True})

    @action(
        detail=True,
        methods=['PUT'],
        serializer_class=FeedbackSerializer
    )
    def give_feedback(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"result": serializer.data})

    @action(
        detail=True,
        methods=['GET'],
        serializer_class=TaskCommentSerializer,
    )
    def comments(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=int(self.kwargs.get('pk')))
        internal_chat = request.query_params.get('internal_chat')
        queryset = task.comments.filter(internal_chat=False)
        if internal_chat is not None and (
            internal_chat or internal_chat == 'true'
        ):
            queryset = task.comments.filter(internal_chat=True)
        serializer = self.serializer_class(queryset, many=True)
        return Response({'count': queryset.count(), 'results': serializer.data})

    
class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @action(
        detail=True,
        methods=['POST'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def purchase(self, request, *args, **kwargs):
        service = self.get_object()
        title = request.data.get('title')
        description = request.data.get('description')
        Project.objects.create(
            user=request.user, title=title, description=description, service=service, workspace=service.workspace
        )
        Transaction.objects.create(
            user=request.user, workspace=service.workspace, service=service, amount=service.price
        )
        WorkspaceMember.objects.get_or_create(
            workspace=service.workspace, user=request.user
        )
        return Response({'success': True})


class CaseStudyViewSet(viewsets.ModelViewSet):
    queryset = CaseStudy.objects.all()
    serializer_class = CaseStudySerializer
    permission_classes = (permissions.IsAuthenticated,)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)


class TaskCommentViewSet(viewsets.ModelViewSet):
    queryset = TaskComment.objects.all()
    serializer_class = TaskCommentSerializer
    permission_classes = (permissions.IsAuthenticated,)


# class TaskCommentViewSet(viewsets.ModelViewSet):
    # queryset = TaskComment.objects.all()
    # serializer_class = TaskCommentSerializer
    # permission_classes = (permissions.IsAuthenticated,)