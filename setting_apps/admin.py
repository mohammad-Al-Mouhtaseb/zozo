from django.contrib import admin
from . models import *

from django.contrib.admin.models import LogEntry
# Register your models here.
admin.site.register(Data)
admin.site.register(LogEntry)