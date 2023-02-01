from django.contrib import admin

from .models import AmountIngredients, Ingredient, Recipe, Tag


class RecipeAdmin(admin.ModelAdmin):
    readonly_fields = ('add_to_favorite',)
    list_display = ('name', 'author',)
    search_fields = ('author', 'name', 'tags')

    def add_to_favorite(self, instance):
        return instance.favorite_recipes.count()


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(AmountIngredients)
