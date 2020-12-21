from django.contrib import admin
from .models import HomeMenu, HomeMenuPermission

# Register your models here.
admin.site.register(HomeMenu)
admin.site.register(HomeMenuPermission)
