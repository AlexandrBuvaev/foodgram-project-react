import base64
from django.core.files.base import ContentFile
from rest_framework import serializers

from recipes.models import Tag, Ingridient, Recipe, AmountIngridients
from users.models import CustomUser
from djoser.serializers import UserSerializer


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


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
    image = Base64ImageField(required=False, allow_null=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )

    class Meta:
        model = Recipe
        fields = (
            'tags', 'author', 'ingridients',
            'image', 'name', 'text', 'cooking_time',
        )

    def create(self, validated_data):
        ingridients = validated_data.pop('ingridients')
        recipe = Recipe.objects.create(**validated_data)
        obj = [AmountIngridients(
            ingridient=Ingridient.objects.get(id=ing['id']),
            recipe=recipe,
            amount=ing['amount']
        ) for ing in ingridients]
        AmountIngridients.objects.bulk_create(obj)
        return recipe
