from rest_framework import viewsets, status
from .serializers import (TagSerializer, IngridientSerializer,
                          SubscribeSerializer)
from rest_framework.response import Response
from recipes.models import Tag, Ingridient
from djoser.views import UserViewSet
from users.models import CustomUser, Subscribe
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для тега."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngridientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет для ингридиентов.
    Доступны только GET запросы
    на /ingridients/ и /ingridients/{pk}/.
    """
    queryset = Ingridient.objects.all()
    serializer_class = IngridientSerializer


class CustomUserViewSet(UserViewSet):
    """Кастомный вью-сет для пользователя."""
    pass

    # def get_subscriptions(self, request):
    #     pass


class SubscribeViewSet(viewsets.ViewSet):
    """Вьюсет для создания и удаления подписки."""

    def create(self, request, user_id):
        """Создание подписки."""
        author = get_object_or_404(CustomUser, pk=user_id)
        if request.user != author:
            try:
                Subscribe.objects.create(author=author, user=request.user)
                serializer = SubscribeSerializer(author,
                                                 context={'request': request})
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"message":
                                "Нельзя подписаться на пользователя дважды."},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Нельзя подписатся на самого себя."},
                        status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, user_id):
        """Удаление подписки."""
        Subscribe.objects.filter(
            user=request.user, author__id=user_id).delete()
        return Response({"message": "Подписка удалена."},
                        status=status.HTTP_204_NO_CONTENT)
