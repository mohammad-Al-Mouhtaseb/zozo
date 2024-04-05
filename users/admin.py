from django.contrib import admin
from . models import *
from .models import User

# admin.site.register(User)
admin.site.register(Patient)
admin.site.register(Doctor)

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    pass