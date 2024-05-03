from django.urls import path
from . import views

urlpatterns = [
    path('firstquiz',views.firstquiz,name='firstquiz'),
    path('Panic_Disorder',views.Panic,name='Panic_Disorder'),
    path('QPanic_Disorder',views.QPanic,name='QPanic_Disorder'),
    path('Panic_view',views.doctor_view,name='doctor_view'),
    path('select_doctor',views.select_doctor,name='select_doctor'),
]
