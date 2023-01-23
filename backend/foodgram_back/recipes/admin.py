from django.contrib import admin
from .models import Ingridient, Tag, Recipe, AmountIngridients


admin.site.register(Tag)
admin.site.register(Ingridient)
admin.site.register(Recipe)
admin.site.register(AmountIngridients)
