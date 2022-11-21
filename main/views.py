from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, TagSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import permissions
from rest_framework.generics import ListAPIView
from rest_framework import viewsets




class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_permissions(self):
        if self.action in ['list', ]:
            self.permission_classes = [permissions.AllowAny, ]
        elif self.action in ['update', 'partial_update', 'destroy', 'list', 'create', 'create', ]:
            self.permission_classes = [permissions.IsAdminUser, ]
        else:
            self.permission_classes = [permissions.AllowAny, ]
        return super(self.__class__, self).get_permissions()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['list', 'create', ]:
            self.permission_classes = [permissions.AllowAny, ]
        elif self.action in ['update', 'partial_update', 'destroy', 'list', 'create', ]:
            self.permission_classes = [permissions.IsAdminUser, ]
        else:
            self.permission_classes = [permissions.AllowAny, ]
        return super(self.__class__, self).get_permissions()

    def get_queryset(self):
        queryset = Comment.objects.filter(post_id=self.kwargs.get('post_id'))
        return queryset

    def perform_create(self, serializer):
        serializer.save(post_id=self.kwargs.get('post_id'))


class TagListView(ListAPIView):
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = Post.objects.filter(tags__name__in=[self.kwargs.get('tag')])
        return queryset
