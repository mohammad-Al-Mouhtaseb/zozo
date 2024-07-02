from django.contrib import admin
from . models import *

class CustomUserAdmin(admin.ModelAdmin):
    exclude = ('is_superuser','user_permissions','last_login','token','private_key')
admin.site.register(User, CustomUserAdmin)


admin.site.register(Patient, CustomUserAdmin)
admin.site.register(Doctor, CustomUserAdmin)
