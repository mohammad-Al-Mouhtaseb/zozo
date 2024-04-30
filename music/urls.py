from django.urls import path
from . import views

urlpatterns = [
    path('<str:name>',views.test,name='music_test'),
    path('create/<str:text>',views.create,name='music_create'),
]