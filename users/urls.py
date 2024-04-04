from django.urls import path
from . import views

urlpatterns = [
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('edit',views.edit,name='edit'),
    path('photo/<int:id>',views.photo,name='photo'),
    path('profile/<int:id>',views.get_profile,name='get_profile'),
    path('get_doctor_list',views.get_doctor_list,name='get_doctor_list'),
    path('add-rate',views.reating,name='reating'),
]
