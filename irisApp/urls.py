from django.urls import path
from . import views

urlpatterns = [
    path('firstquiz',views.firstquiz,name='firstquiz'),

    path('panic_pisorder',views.Panic,name='Panic_Disorder'),
    path('dep_bi',views.Dep_Bi,name='Dep_Bi'),
    path('p_dep',views.P_Dep,name='P_Dep'),
    
    path('q_panic_disorder',views.QPanic,name='QPanic_Disorder'),
    path('q_dep_bi',views.QDep_Bi,name='QDep_Bi'),
    path('q_p_dep',views.QP_Dep,name='QP_Dep'),


    path('select_doctor',views.select_doctor,name='select_doctor'),
    path('show_my_patient',views.patient_list_for_doctor,name='patient_list_for_doctor'),
    path('doctor_view_data',views.doctor_view,name='doctor_view'),
]