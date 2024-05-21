from django.urls import path
from . import views

urlpatterns = [
    # path('music/gen',views.m_gen,name='m_gen'),
    # path('music/get_my_list',views.m_get_my_list,name='m_get_my_list'),
    # path('music/get_folder_list',views.m_get_folder_list,name='m_get_folder_list'),
    # path('music/get_music',views.m_get_music,name='m_get_music'),
    path('quran/surahList',views.q_surahList,name='q_surahList'),
    path('quran/surah_audio/<str:name>',views.q_surah_audio,name='q_surah_audio')
]
