from rest_framework import serializers

from recipes.models import Tag, Ingridient, Recipe
from users.models import CustomUser
from djoser.serializers import UserSerializer


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
                'email', 'id', 'username', 'first_name',
                'last_name', 'is_subscribed'
            )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return user.subscriber.filter(author=obj).exists()


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngridientSerializer(serializers.ModelSerializer):
    """Сериализатор ингридиентов."""

    class Meta:
        model = Ingridient
        fields = ('id', 'name', 'measurement_unit')


class AmountIngridientSerializer(IngridientSerializer):
    """Сериализатор для добавления ингредиентов в рецепт."""
    amount = serializers.IntegerField(required=True)

    class Meta:
        model = Ingridient
        fields = (
            'id', 'amount'
        )


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов."""
    author = CustomUserSerializer(read_only=True)
    ingridients = AmountIngridientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'tags', 'author', 'ingridients',
            'image', 'name', 'text', 'cooking_time',
        )
