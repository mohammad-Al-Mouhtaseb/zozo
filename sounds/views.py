from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, FileResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import requests, json
from . models import *

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

@csrf_exempt
def q_surahList(request):
    url = "https://online-quran-api.p.rapidapi.com/surahs"
    headers = {
        "X-RapidAPI-Key": "4120ca7630msh5566122415863dep16069fjsn207bd1f0e6f4",
        "X-RapidAPI-Host": "online-quran-api.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    surahList = response.json()['surahList']
    res=[]
    for i in surahList:
        res.append(i["name"])
    return JsonResponse({"surahList":res})

@csrf_exempt
def q_surah_audio(request,name):
    url = "https://online-quran-api.p.rapidapi.com/surahs/"+name
    headers = {
        "X-RapidAPI-Key": "4120ca7630msh5566122415863dep16069fjsn207bd1f0e6f4",
        "X-RapidAPI-Host": "online-quran-api.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    return JsonResponse({"audio":response.json()['audio']})