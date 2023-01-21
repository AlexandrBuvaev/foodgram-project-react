from django.urls import path, include
from .views import (TagViewSet, IngridientViewSet,
                    CustomUserViewSet, SubscribeViewSet)
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='users')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingridients', IngridientViewSet, basename='ingridient')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/subscribe/<int:user_id>/',
         SubscribeViewSet.as_view({'post': 'create', 'delete': 'destroy'}),
         name='subscribe')
]
