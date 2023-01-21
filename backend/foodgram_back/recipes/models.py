from django.db import models
# from users.models import CustomUser


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


# class Recipe(models.Model):
#     """
#     Модель рецепта.
#     """
#     author = models.ForeignKey(
#         CustomUser, "Автор",
#         on_delete=models.CASCADE,
#         related_name='recipes'
#     )
#     name = models.CharField("Название", max_length=150)
#     image = models.ImageField(
#         "Картинка", upload_to='recipes/images',
#     )
#     text = models.TextField("Текстовое описание", max_length=150)
#     tag = models.ForeignKey(Tag, "Тег", on_delete=models.CASCADE)
#     ingridients = models.ManyToManyField('Ingridients',
#                                          through='RecipeIngridients')
#     coocking_time = models.IntegerField("Время приготовления")


class Ingridient(models.Model):
    """
    Модель ингридиента.
    """
    name = models.CharField("Название", max_length=150)
    measurement_unit = models.CharField("Единица измерния", max_length=50)

    class Meta:
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"

    def __str__(self):
        return self.name

# class RecipeIngridients(models.Model):
#     """Связывающая модель рецептов и ингридиентов."""
#     recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
#     ingridient = models.ForeignKey(Ingridient, on_delete=models.CASCADE)
