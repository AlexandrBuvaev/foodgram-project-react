from django.urls import path, include
from .views import (TagViewSet, IngridientViewSet,
                    CustomUserViewSet, SubscribeViewSet,
                    RecipeViewSet, FavoriteRecipesViewSet,
                    ShoppingCartRecipesViewSet)
from rest_framework import routers


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
