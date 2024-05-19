from rest_framework.response import Response
from rest_framework import status, viewsets


class BasePostCommentViewSet(viewsets.ModelViewSet):
    """Базовый класс для работы с постами и комментариями."""
    def check_author(self, request, obj):
        """Проверяет, является ли пользователь автором объекта."""
        if obj.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        """ Метод для удаления объекта."""
        obj = self.get_object()
        response = self.check_author(request, obj)
        if response:
            return response
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Метод для обновления объекта."""
        obj = self.get_object()
        response = self.check_author(request, obj)
        if response:
            return response
        return super().update(request, *args, **kwargs)
