from django.contrib import admin
from . models import *

class CustomUser(admin.ModelAdmin):
    exclude = ('is_superuser','user_permissions','last_login','token','private_key','date_joined')
admin.site.register(User, CustomUser)

class CustomPatient(admin.ModelAdmin):
    exclude = ('is_superuser','user_permissions','last_login','token','private_key','groups','type','is_staff','name','date_joined')
admin.site.register(Patient, CustomPatient)

class CustomDoctor(admin.ModelAdmin):
    exclude = ('is_superuser','user_permissions','last_login','token','private_key','groups','type','is_staff','num_of_rate','name','date_joined')
admin.site.register(Doctor, CustomDoctor)
