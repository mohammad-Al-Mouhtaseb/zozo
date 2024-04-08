from django.contrib import admin
from . models import *

admin.site.register(Patient)
admin.site.register(Doctor)

class CustomUserAdmin(admin.ModelAdmin):
    pass
    # exclude = ('photo','password','is_active','is_superuser','is_staff','user_permissions','groups')
admin.site.register(User, CustomUserAdmin)
