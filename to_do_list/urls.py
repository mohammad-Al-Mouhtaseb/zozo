from django.urls import path
from . import views

urlpatterns = [
    path('set', views.set_to_do_list, name='set_to_do_list'),
    path('get', views.get_to_do_list, name='get_to_do_list'),
]
