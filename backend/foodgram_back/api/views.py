from rest_framework import viewsets, status
from .serializers import (TagSerializer, IngridientSerializer,
                          CustomUserSerializer, RecipeSerializer)
from rest_framework.response import Response
from recipes.models import Tag, Ingridient, Recipe
from djoser.views import UserViewSet
from users.models import CustomUser, Subscribe
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from rest_framework.decorators import action


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


class RecipeViewSet(viewsets.ModelViewSet):
    """Вью-сет для рецептов."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class CustomUserViewSet(UserViewSet):
    """Кастомный вью-сет для пользователя."""

    @action(detail=False,
            methods=['get'],
            url_name='subscriptions',
            url_path='subscriptions')
    def get_subscriptions(self, request):
        queryset = self.get_queryset().filter(
            subscribing__user=request.user
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CustomUserSerializer(page,
                                              context={'request': request},
                                              many=True)
            return self.get_paginated_response(serializer.data)


class SubscribeViewSet(viewsets.ViewSet):
    """Вьюсет для создания и удаления подписки."""

    def create(self, request, user_id):
        """Создание подписки."""
        author = get_object_or_404(CustomUser, pk=user_id)
        if request.user != author:
            try:
                Subscribe.objects.create(author=author, user=request.user)
                serializer = CustomUserSerializer(author,
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
