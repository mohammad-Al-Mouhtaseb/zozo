from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat, name='chat'),
    path('network', views.get_my_network, name='get_my_network'),
]
