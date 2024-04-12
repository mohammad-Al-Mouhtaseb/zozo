from django.urls import path
from . import views

urlpatterns = [
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('edit',views.edit,name='edit'),
    path('photo/<str:email>',views.photo,name='photo'),
    path('upload_photo/<str:email>',views.upload_photo,name='upload_photo'),
    path('profile/<str:email>',views.get_profile,name='get_profile'),
    path('get_doctor_list',views.get_doctor_list,name='get_doctor_list'),
    path('add-rate',views.reating,name='reating'),
    path('auth',views.auth,name='auth'),
]
