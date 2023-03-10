import base64

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from djoser.serializers import UserSerializer
from rest_framework import serializers, status

from recipes.models import (AmountIngredients, FavoriteRecipes, Ingredient,
                            Recipe, ShoppingCart, Tag)
from users.models import CustomUser, Subscribe


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
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return user.subscriber.filter(author=obj).exists()


class SubscribeSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed', 'recipes', 'recipes_count'
        )
        read_only_fields = (
            'email', 'username', 'first_name', 'last_name'
        )

    def get_recipes(self, obj):
        recipes_limit = int(
            self.context['request'].query_params.get('recipes_limit', 3)
        )
        recipes = obj.recipes.all()
        if isinstance(recipes_limit, int):
            serializer = SmallRecipeSerializer(
                recipes[:recipes_limit], many=True)
        else:
            raise serializers.ValidationError(
                "recipes_limit ???????????? ????????  ?????????? ????????????.")
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def validate(self, data):
        author = self.instance
        user = self.context['request'].user
        if Subscribe.objects.filter(author=author, user=user).exists():
            raise serializers.ValidationError(
                detail='???????????? ?????????????????????? ???? ???????????????????????? ????????????.',
                code=status.HTTP_400_BAD_REQUEST
            )
        if user == author:
            raise serializers.ValidationError(
                detail='???????????? ?????????????????????? ???? ???????????? ????????.',
                code=status.HTTP_400_BAD_REQUEST
            )
        return data


class TagSerializer(serializers.ModelSerializer):
    """???????????????????????? ??????????."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """???????????????????????? ????????????????????????."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class AmountIngredientSerializer(serializers.ModelSerializer):
    """???????????????????????? ?????? ???????????????????? ???????????????????????? ?? ????????????."""
    id = serializers.IntegerField()

    class Meta:
        model = AmountIngredients
        fields = (
            'id', 'amount'
        )


class FullAmountIngredientSerializer(serializers.ModelSerializer):
    """???????????????????????? ?????? ???????????????????? ???????????????????????? ?? ????????????."""
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = AmountIngredients
        fields = (
            'id', 'name', 'measurement_unit', 'amount'
        )


class SmallRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id', 'image', 'name', 'cooking_time',
        )
        read_only_fields = ('name', 'cooking_time')


class FavoriteRecipeSerializer(SmallRecipeSerializer):
    """???????????????????????? ????????????????."""

    def validate(self, data):
        recipe = self.instance
        user = self.context['request'].user
        if FavoriteRecipes.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError(
                detail='???????????? ?????? ?? ??????????????????.',
                code=status.HTTP_400_BAD_REQUEST
            )
        return data


class ShoppingCartRecipeSerializer(SmallRecipeSerializer):
    """???????????????????????? ????????????????."""

    def validate(self, data):
        recipe = self.instance
        user = self.context['request'].user
        if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError(
                detail='???????????? ?????? ?? ??????????????.',
                code=status.HTTP_400_BAD_REQUEST
            )
        return data


class FullRecipeSerializer(serializers.ModelSerializer):
    """???????????????????????? ????????????????."""
    author = CustomUserSerializer(read_only=True)
    ingredients = FullAmountIngredientSerializer(read_only=True, many=True)
    image = Base64ImageField()
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'author',
            'image', 'name', 'text', 'cooking_time',
        )

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return user.favorite_recipes.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return user.shopping_cart.filter(recipe=obj).exists()


def set_ingredients(data):
    """?????????????? ?????? ???????????????????? ???????????????????????? ?? ????????????."""
    amount_ingredients = []
    for new_ingredient in data:
        ingredient = get_object_or_404(
            Ingredient,
            pk=new_ingredient['id']
        )
        amount_ingredient, created = (
            AmountIngredients.objects.get_or_create(
                ingredient=ingredient,
                amount=new_ingredient['amount']
            )
        )
        amount_ingredient.save()
        amount_ingredients.append(amount_ingredient)
    return amount_ingredients


class RecordRecipeSerializer(serializers.ModelSerializer):
    """???????????????????????? ????????????????."""
    author = CustomUserSerializer(read_only=True)
    ingredients = AmountIngredientSerializer(many=True)
    image = Base64ImageField(required=False, allow_null=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )

    class Meta:
        model = Recipe
        fields = (
            'tags', 'ingredients', 'author',
            'image', 'name', 'text', 'cooking_time',
        )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.ingredients.set(set_ingredients(data=ingredients))
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        if 'tags' in validated_data:
            tags_data = validated_data.pop('tags')
            instance.tags.set(tags_data)
        if 'ingredients' in validated_data:
            ingredients = validated_data.pop('ingredients')
            instance.ingredients.set(set_ingredients(data=ingredients))

        instance.save()
        return instance
