from django.db import models

from users.models import CustomUser


class Tag(models.Model):
    """
    Модель для представления тега.
    Рецепты могут содержат в себе теги и их можно разделять по тегам.
    """
    name = models.CharField("Название", max_length=50)
    color = models.CharField("Код цвет в НЕХ формате", max_length=16)
    slug = models.SlugField('Слаг тега', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
    Модель рецепта.
    """
    ingredients = models.ManyToManyField(
        'AmountIngredients'
    )
    name = models.CharField("Название", max_length=200)
    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор',
        related_name='recipes',
        on_delete=models.CASCADE
    )
    text = models.TextField("Описание", max_length=250)
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(
        "Изображение",
        upload_to='recipes/images/',
        null=True,
        default=None
    )
    cooking_time = models.IntegerField("Время приготовления.")

    class Meta:
        ordering = ('-pk',)
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Модель ингридиента.
    """
    name = models.CharField("Название", max_length=150)
    measurement_unit = models.CharField("Единица измерния", max_length=50)

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name


class AmountIngredients(models.Model):
    """Связывающая модель рецептов и ингридиентов."""
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name="Название ингредиента",
        related_name='ingredient_recipe',
        on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество'
    )

    def __str__(self):
        return f'{self.ingredient} {self.amount}'

    class Meta:
        verbose_name = "Количество ингредиентов"
        verbose_name_plural = "Количества ингериентов в рецептах"


class FavoriteRecipes(models.Model):
    """Избранные рецепты."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='Пользователь'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_user_favorite_recipe'
            )
        ]

    def __str__(self):
        return self.recipe


class ShoppingCart(models.Model):
    """Корзина."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )

    class Meta:
        verbose_name = 'Рецепт в корзине'
        verbose_name_plural = 'Рецепты в корзине'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_user_shopping_cart'
            )
        ]

    def __str__(self):
        return f'{self.recipe.name}'
