from django.contrib import admin
from . models import CustomUser, Subscribe

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Subscribe)
