from django.urls import path
from . import views

urlpatterns = [
    path('music/gen',views.gen,name='gen'),
    path('music/get_music',views.get_music,name='get_music'),
    path('music/get_my_list',views.get_my_list,name='get_my_list'),
    path('music/get_folder_list',views.get_folder_list,name='get_folder_list'),
    path('quran/surahList',views.q_surahList,name='q_surahList'),
    path('quran/surah_audio/<str:name>',views.q_surah_audio,name='q_surah_audio')
]
