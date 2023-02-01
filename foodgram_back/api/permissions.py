from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Ограничение, которое позволяет редактировать,
    частично редактировать и удалять рецепты только авторам
    этих рецептов.
    """
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )