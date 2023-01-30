from django.urls import include, path
from rest_framework import routers

from .views import (CustomUserViewSet, FavoriteRecipesViewSet,
                    IngridientViewSet, RecipeViewSet,
                    ShoppingCartRecipesViewSet, SubscribeViewSet, TagViewSet)

router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='users')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingridients', IngridientViewSet, basename='ingridient')
router.register(r'recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/<int:user_id>/subscribe/',
         SubscribeViewSet.as_view({'post': 'create', 'delete': 'destroy'}),
         name='subscribe'),
    path(
        'recipes/<int:recipe_id>/favorite/',
        FavoriteRecipesViewSet.as_view(
            {'post': 'create', 'delete': 'destroy'}
        ),
        name='favorite'
    ),
    path(
        'recipes/<int:recipe_id>/shopping_cart/',
        ShoppingCartRecipesViewSet.as_view(
            {'post': 'create', 'delete': 'destroy'}
        ),
        name='shopping_cart'
    )
]
