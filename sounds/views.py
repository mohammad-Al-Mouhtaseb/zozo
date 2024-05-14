# from django.shortcuts import render
# from django.http import HttpResponseRedirect
# from django.views.decorators.csrf import csrf_exempt

# # Create your views here.

# music_ip="http://127.0.0.1:5000/"

# @csrf_exempt
# def m_gen(request):
#     url=music_ip+"music/gen"
#     return HttpResponseRedirect(redirect_to=url)

# @csrf_exempt
# def m_get_my_list(request):
#     url=music_ip+"music/get_my_list"
#     return HttpResponseRedirect(redirect_to=url)

# @csrf_exempt
# def m_get_folder_list(request):
#     url=music_ip+"music/get_folder_list"
#     return HttpResponseRedirect(redirect_to=url)

# @csrf_exempt
# def m_get_music(request):
#     url=music_ip+"music/get_music"
#     return HttpResponseRedirect(redirect_to=url)

# @csrf_exempt
# def q_surahList(request):
#     url=music_ip+"music/surahList"
#     return HttpResponseRedirect(redirect_to=url)

# @csrf_exempt
# def q_surah_audio(request,name):
#     url=music_ip+"music/surah_audio"+name
#     return HttpResponseRedirect(redirect_to=url)
