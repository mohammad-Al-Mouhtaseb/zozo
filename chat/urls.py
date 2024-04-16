from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat, name='chat'),
    # # path('msgs', views.chatall, name='chatall'),
    path('network', views.get_my_network, name='get_my_network'),
    # path('translate', views.translate, name='translate'),
    path('note/<str:channel>', views.note, name='note'),
]
