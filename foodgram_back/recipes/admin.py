from django.contrib import admin

from .models import AmountIngridients, Ingridient, Recipe, Tag

admin.site.register(Tag)
admin.site.register(Ingridient)
admin.site.register(Recipe)
admin.site.register(AmountIngridients)