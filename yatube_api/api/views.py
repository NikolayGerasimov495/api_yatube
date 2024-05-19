from rest_framework import viewsets, status
from rest_framework.response import Response

from posts.models import Comment, Group, Post
from .base_post_comment_viewset import BasePostCommentViewSet
from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с группами."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def method_not_allowed(self, request, *args, **kwargs):
        """Метод для возврата ошибки Method Not Allowed."""
        return Response({"error": "Method Not Allowed"},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    create = update = partial_update = destroy = method_not_allowed


class PostViewSet(BasePostCommentViewSet):
    """ViewSet для работы с постами."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        """Метод для создания нового поста."""
        serializer.save(author=self.request.user)


class CommentViewSet(BasePostCommentViewSet):
    """ViewSet для работы с комментариями."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, post_id=None):
        """Метод для получения списка комментариев к посту."""
        comments = Comment.objects.filter(post=post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """Метод для создания нового комментария."""
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(id=post_id)
        serializer.save(author=self.request.user, post=post)
