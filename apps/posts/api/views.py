from django.utils import timezone
from django.shortcuts import get_object_or_404
from apps.posts.api.serializers import *
from apps.posts.models import *
from apps.workspace.helpers import invite_mail
from django.contrib.auth import authenticate

from rest_framework.decorators import action
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Post.objects.filter(user=self.request.user)
        return queryset
    
    def create(self, request, *args, **kwargs):
        tags = request.data.get("tag_list", [])
        options = request.data.get("option_list", [])
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            for tag in list(tags):
                PostTag.objects.create(
                    post_id=serializer.data.get('id'), tag=tag
                )
            
            for option in list(options):
                PollOption.objects.create(
                    post_id=serializer.data.get('id'), text=option
                )

        return Response(serializer.data)

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=(permissions.AllowAny,),
    )
    def all(self, request, *args, **kwargs):
        queryset = Post.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response({'count': queryset.count(), 'results': serializer.data})
    
    @action(
        detail=True,
        methods=['PUT'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def pin(self, request, *args, **kwargs):
        post = self.get_object()
        post.is_pinned = True
        post.save()
        return Response({"success": True})
    
    @action(
        detail=True,
        methods=['PUT'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def unpin(self, request, *args, **kwargs):
        post = self.get_object()
        post.is_pinned = False
        post.save()
        return Response({"success": True})
    
    @action(
        detail=True,
        methods=['PUT'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def like(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs.get('pk'))
        PostLike.objects.get_or_create(post=post, user=request.user)
        return Response({"success": True})
    
    @action(
        detail=True,
        methods=['PUT'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def unlike(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs.get('pk'))
        PostLike.objects.filter(post=post, user=request.user).delete()
        return Response({"success": True})
    
    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def search(self, request, *args, **kwargs):
        tag = request.query_params.get('tag', None)

        if tag is not None and PostTag.objects.filter(tag=tag).exists():
            queryset = Post.objects.filter(tags__tag=tag)
            serializer = self.serializer_class(queryset, many=True)
            return Response({'count': queryset.count(), 'results': serializer.data})
        return Response({'results': []})
    

    @action(
        detail=True,
        methods=['GET'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def all_comments(self, request, *args, **kwargs):
        post = self.get_object()
        queryset = post.comments.all()
        serializer = PostCommentSerializer(queryset, many=True)
        return Response({'results': serializer.data})
    

    @action(
        detail=True,
        methods=['PUT'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def poll(self, request, *args, **kwargs):
        poll = get_object_or_404(PollOption, pk=kwargs.get('pk'))
        poll.vote = int(poll.vote) +1
        poll.save()
        return Response({"success": True})


class PostCommentViewSet(viewsets.ModelViewSet):
    serializer_class = PostCommentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = PostComment.objects.filter(user=self.request.user)
        return queryset