from django.contrib import admin
from .models import Ingridient, Tag, Recipe


admin.site.register(Tag)
admin.site.register(Ingridient)
admin.site.register(Recipe)
