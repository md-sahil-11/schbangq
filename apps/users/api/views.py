from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate

from rest_framework.decorators import action
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from apps.users.api.serializers import UserRewardSerializer, UserSerializer

from apps.users.models import Follow, User

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=(permissions.AllowAny,),
    )
    def login(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if not user:
            return Response({"success": False, "err": "Invalid password or email!"})
        if not user.is_active:
            return Response(
                {
                    "success": False,
                    "err": "Please open verification link sent on this email to continue!",
                }
            )
        data = UserSerializer(user).data
        return Response({"success": True, "data": data})

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=(permissions.AllowAny,),
    )
    def register(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")
        if password == confirm_password:
            if User.objects.filter(email = email):
                return Response({"success": False, "err": "Email already exists!"})
            else:
                user = User.objects.create_user(email=email, password=password)
                user.save()
                return Response({"success": True, "data": UserSerializer(user).data})

    @action(
        detail=False,
        methods=["GET"],
        serializer_class=UserRewardSerializer,
        permission_classes=(permissions.IsAuthenticated,),
    )
    def rewards(self, request, *args, **kwargs):
        queryset = request.user.rewards.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response({"count": queryset.count(), "results": serializer.data})

    @action(
        detail=True,
        methods=["GET"],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def follow(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=int(self.kwargs.get('pk')))
        Follow.objects.get_or_create(
            followed=user, follower=request.user
        )
    
    @action(
        detail=True,
        methods=["GET"],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def unfollow(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=int(self.kwargs.get('pk')))
        Follow.objects.filter(
            followed=user, follower=request.user
        ).delete()







