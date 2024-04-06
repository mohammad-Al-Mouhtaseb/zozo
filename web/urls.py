from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('googlef07a8177d651b4db.html',views.google_search,name='google-search'),
]
