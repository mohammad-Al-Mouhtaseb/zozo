from django.urls import path
from . import views
from . import photos

urlpatterns = [
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('edit',views.edit,name='edit'),
    path('photo/<str:text>',views.photo,name='photo'),
    path('photos/<str:text>',views.photo,name='photo'),
    path('upload_photo/<str:email>',views.upload_photo,name='upload_photo'),
    path('profile/<str:email>',views.get_profile,name='get_profile'),
    path('get_doctor_list',views.get_doctor_list,name='get_doctor_list'),
    path('add-rate',views.reating,name='reating'),
    path('auth/<str:email>/<str:token>',views.auth,name='auth'),
    path('public_key/<str:email>',views.get_public_key,name='get_public_key'),
]