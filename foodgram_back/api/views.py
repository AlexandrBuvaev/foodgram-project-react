from io import StringIO

from django.db.models import Sum
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.models import (AmountIngridients, FavoriteRecipes, Ingridient,
                            Recipe, ShoppingCart, Tag)
from users.models import CustomUser, Subscribe

from .serializers import (CustomUserSerializer, FullRecipeSerializer,
                          IngridientSerializer, RecordRecipeSerializer,
                          SmallRecipeSerializer, SubscribeSerializer,
                          TagSerializer)


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
    serializer_class = FullRecipeSerializer

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return RecordRecipeSerializer
        return FullRecipeSerializer

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    @action(
        detail=False,
        methods=['get'],
        url_name='download_shopping_cart',
        url_path='download_shopping_cart'
    )
    def download_shopping_cart(self, request):
        queryset = AmountIngridients.objects.filter(
            recipe__shopping_cart__user=self.request.user
        )
        shopping_cart = queryset.values('ingridient').annotate(
            total_amount=Sum('amount')
        )
        shopping_cart_file = StringIO()
        for position in shopping_cart:
            position_ingridient = get_object_or_404(
                Ingridient,
                pk=position['ingridient']
            )
            position_amount = position['total_amount']
            shopping_cart_file.write(
                f' *  {position_ingridient.name.title()}'
                f' ({position_ingridient.measurement_unit})'
                f' - {position_amount}' + '\n'
            )
        response = HttpResponse(
            shopping_cart_file.getvalue(),
            content_type='text'
        )
        response['Content-Disposition'] = (
            'attachment; filename="%s"' % 'shopping_list.txt'
        )
        return response


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
            serializer = SubscribeSerializer(page,
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


class FavoriteRecipesViewSet(viewsets.ViewSet):
    """Добавление рецепта в избранное."""

    def create(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        try:
            FavoriteRecipes.objects.create(
                recipe=recipe, user=request.user
            )
            serializer = SmallRecipeSerializer(
                recipe, context={'request': request}
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        except IntegrityError:
            return Response(
                {"message": 'Нельзя добавить рецепт в избранное дважды.'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, recipe_id):
        FavoriteRecipes.objects.filter(
            user=request.user, recipe__id=recipe_id
        ).delete()
        return Response(
            {'message': 'Рецепт удален из избранного.'},
            status=status.HTTP_204_NO_CONTENT
        )


class ShoppingCartRecipesViewSet(viewsets.ViewSet):
    """Добавление и удаление рецептов в корзину."""
    def create(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        try:
            ShoppingCart.objects.create(
                recipe=recipe, user=request.user
            )
            serializer = SmallRecipeSerializer(
                recipe, context={'request': request}
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        except IntegrityError:
            return Response(
                {"message": 'Нельзя добавить рецепт в избранное дважды.'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, recipe_id):
        ShoppingCart.objects.filter(
            user=request.user, recipe__id=recipe_id
        ).delete()
        return Response(
            {'message': 'Рецепт удален из избранного.'},
            status=status.HTTP_204_NO_CONTENT
        )
