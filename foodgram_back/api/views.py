from io import StringIO

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response

from recipes.models import (AmountIngredients, FavoriteRecipes, Ingredient,
                            Recipe, ShoppingCart, Tag)
from users.models import CustomUser, Subscribe

from .filters import IngredientsFilterBackend, RecipeFilterBackend
from .pagination import PageLimitPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (FullRecipeSerializer,
                          IngredientSerializer, RecordRecipeSerializer,
                          SmallRecipeSerializer, SubscribeSerializer,
                          TagSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для тега."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет для ингридиентов.
    Доступны только GET запросы
    на /ingridients/ и /ingridients/{pk}/.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientsFilterBackend, )
    search_fields = ('^name', 'name')


class RecipeViewSet(viewsets.ModelViewSet):
    """Вью-сет для рецептов."""
    queryset = Recipe.objects.all()
    serializer_class = FullRecipeSerializer
    filter_backends = (RecipeFilterBackend, )
    pagination_class = PageLimitPagination
    permission_classes = (IsAuthorOrReadOnly, )

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
        url_path='download_shopping_cart',
        permission_classes=(IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        queryset = AmountIngredients.objects.filter(
            recipe__shopping_cart__user=self.request.user
        )
        shopping_cart = queryset.values('ingredient').annotate(
            total_amount=Sum('amount')
        )
        shopping_cart_file = StringIO()
        for position in shopping_cart:
            position_ingredient = get_object_or_404(
                Ingredient,
                pk=position['ingredient']
            )
            position_amount = position['total_amount']
            shopping_cart_file.write(
                f' *  {position_ingredient.name.title()}'
                f' ({position_ingredient.measurement_unit})'
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
    pagination_class = PageLimitPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @action(detail=False,
            methods=['get'],
            url_name='subscriptions',
            url_path='subscriptions',
            permission_classes=(IsAuthenticated,),
            )
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
    permission_classes = (IsAuthenticated,)

    def create(self, request, user_id):
        """Создание подписки."""
        author = get_object_or_404(CustomUser, pk=user_id)
        subscribe, created = Subscribe.objects.get_or_create(
            author=author, user=request.user
            )
        # print(subscribe, created)
        if request.user != author and created:
            serializer = SubscribeSerializer(author,
                                             context={'request': request})
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(
            {"message":
             "Нельзя подписатся на самого себя и на пользователя дважды."},
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, user_id):
        """Удаление подписки."""
        Subscribe.objects.filter(
            user=request.user, author__id=user_id).delete()
        return Response({"message": "Подписка удалена."},
                        status=status.HTTP_204_NO_CONTENT)


class FavoriteRecipesViewSet(viewsets.ViewSet):
    """Добавление рецепта в избранное."""
    permission_classes = (IsAuthenticated,)

    def create(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        favorite_recipe, created = FavoriteRecipes.objects.get_or_create(
            recipe=recipe, user=request.user
        )
        if created:
            serializer = SmallRecipeSerializer(
                recipe, context={'request': request}
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
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
    permission_classes = (IsAuthenticated,)

    def create(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        recipe_in_shopping_cart, created = ShoppingCart.objects.get_or_create(
                recipe=recipe, user=request.user
            )
        if created:
            serializer = SmallRecipeSerializer(
                recipe, context={'request': request}
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"message": 'Нельзя добавить рецепт в корзину дважды.'},
            status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, recipe_id):
        ShoppingCart.objects.filter(
            user=request.user, recipe__id=recipe_id
        ).delete()
        return Response(
            {'message': 'Рецепт удален из корзины.'},
            status=status.HTTP_204_NO_CONTENT
        )
