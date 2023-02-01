from django.contrib import admin

from .models import CustomUser, Subscribe


class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ('email', 'username')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Subscribe)
