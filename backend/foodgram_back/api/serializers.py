import base64
from django.core.files.base import ContentFile
from rest_framework import serializers

from recipes.models import Tag, Ingridient, Recipe, AmountIngridients
from users.models import CustomUser
from djoser.serializers import UserSerializer
from django.shortcuts import get_object_or_404


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


class AmountIngridientSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления ингредиентов в рецепт."""
    id = serializers.IntegerField()

    class Meta:
        model = AmountIngridients
        fields = (
            'id', 'amount'
        )


class FullAmountIngridientSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления ингредиентов в рецепт."""
    id = serializers.IntegerField(source='ingridient.id')
    name = serializers.CharField(source='ingridient.name')
    measurement_unit = serializers.CharField(
        source='ingridient.measurement_unit'
    )

    class Meta:
        model = AmountIngridients
        fields = (
            'id', 'name', 'measurement_unit', 'amount'
        )


class FullRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов."""
    author = CustomUserSerializer(read_only=True)
    ingridients = FullAmountIngridientSerializer(read_only=True, many=True)
    image = Base64ImageField(required=False, allow_null=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'tags', 'ingridients', 'author',
            'image', 'name', 'text', 'cooking_time',
        )


class RecordRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов."""
    author = CustomUserSerializer(read_only=True)
    ingridients = AmountIngridientSerializer(many=True)
    image = Base64ImageField(required=False, allow_null=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )

    class Meta:
        model = Recipe
        fields = (
            'tags', 'ingridients', 'author',
            'image', 'name', 'text', 'cooking_time',
        )

    def create(self, validated_data):
        print(validated_data)
        ingridients = validated_data.pop('ingridients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        amount_ingridients = []
        for new_ingridient in ingridients:
            ingridient = get_object_or_404(
                Ingridient,
                pk=new_ingridient['id']
            )
            amount_ingridient, created = (
                AmountIngridients.objects.get_or_create(
                    ingridient=ingridient,
                    amount=new_ingridient['amount']
                )
            )
            if created:
                amount_ingridient.save()
            amount_ingridients.append(amount_ingridient)
        recipe.ingridients.set(amount_ingridients)
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        if 'tags' in validated_data:
            tags_data = validated_data.pop('tags')
            instance.tags.set(tags_data)
        if 'ingridients' in validated_data:
            ingridients = validated_data.pop('ingridients')
            amount_ingridients = []
            for new_ingridient in ingridients:
                ingridient = get_object_or_404(
                    Ingridient,
                    pk=new_ingridient['id']
                )
                amount_ingridient, created = (
                    AmountIngridients.objects.get_or_create(
                        ingridient=ingridient,
                        amount=new_ingridient['amount']
                    )
                )
                if created:
                    amount_ingridient.save()
                amount_ingridients.append(amount_ingridient)
            instance.ingridients.set(amount_ingridients)

        instance.save()
        return instance
