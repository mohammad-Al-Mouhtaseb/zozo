from django.urls import path
from . import views

urlpatterns = [
    path('set', views.set_to_do_list, name='set_to_do_list'),
    path('get', views.get_to_do_list, name='get_to_do_list'),
    path('done-goal', views.done_to_do_goal, name='done_to_do_goal'),
]
