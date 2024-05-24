from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, FileResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import requests, json
from . models import *

# # Create your views here.

# music_ip="http://127.0.0.1:5000/"

# @csrf_exempt
# def m_gen(request):
#     print()
    # url=music_ip+"music/gen"
    # return HttpResponseRedirect(redirect_to=url)

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
    # url = "https://online-quran-api.p.rapidapi.com/surahs"
    # headers = {
    #     "X-RapidAPI-Key": "4120ca7630msh5566122415863dep16069fjsn207bd1f0e6f4",
    #     "X-RapidAPI-Host": "online-quran-api.p.rapidapi.com"
    # }
    # response = requests.get(url, headers=headers)
    # surahList = response.json()['surahList']
    # res=[]
    # for i in surahList:
    #     res.append(i["name"])
    res={
    "surahList": [
        "Surah-Al-Fatihah","Surah-Al-Baqara","Surah-Al-Imran","Surah-An-Nisaa","Surah-Al-Maidah","Surah-Al-An`am","Surah-Al-A`raf","Surah-Al-Anfal","Surah-At-Taubah","Surah-Yunus","Surah-Hud","Surah-Yusuf","Surah-Ar-Ra`d","Surah-Ibrahim","Surah-Al-Hijr","Surah-An-Nahl","Surah-Israel","Surah-Al-Kahf","Surah-Maryam","Surah-Ta-ha","Surah-Al-Anbiyaa","Surah-Al-Hajj","Surah-Al-Muminun","Surah-An-Nur","Surah-Al-Furqan","Surah-Ash-Shu`araa","Surah-An-Naml","Surah-Al-Qasas","Surah-Al-Ankabut","Surah-Ar-Rum","Surah-Luqman","Surah-As-Sajda","Surah-Al-Ahzab","Surah-Saba","Surah-Fatir","Surah-Ya-Sin","Surah-As-Saffat","Surah-Sad","Surah-Az-Zumar","Surah-Al-Mu`min","Surah-Ha-Mim","Surah-Ash-Shura","Surah-Az-Zukhruf","Surah-Ad-Dukhan","Surah-Al-Jathiya","Surah-Al-Ahqaf","Surah-Muhammad","Surah-Al-Fat-h","Surah-Al-Hujurat","Surah-Qaf","Surah-Az-Zariyat","Surah-At-Tur","Surah-An-Najm","Surah-Al-Qamar","Surah-Ar-Rahman","Surah-Al-Waqi`a","Surah-Al-Hadid","Surah-Al-Mujadila","Surah-Al-Hashr","Surah-Al-Mumtahana","Surah-As-Saff","Surah-Al-Jumu`a","Surah-Al-Munafiqun","Surah-At-Tagabun","Surah-At-Talaq","Surah-At-Tahrim","Surah-Al-Mulk","Surah-Al-Qalam","Surah-Al-Haqqa","Surah-Al-Ma`arij","Surah-Nuh","Surah-Al-Jinn","Surah-Al-Muzzammil","Surah-Al-Muddathth","Surah-Al-Qiyamat","Surah-Ad-Dahr","Surah-Al-Mursalat","Surah-An-Nabaa","Surah-An-Nazi`at","Surah-Abasa","Surah-At-Takwir","Surah-Al-Infitar","Surah-Al-Mutaffife","Surah-Al-Inshiqaq","Surah-Al-Buruj","Surah-At-Tariq","Surah-Al-A`la","Surah-Al-Gashiya","Surah-Al-Fajr","Surah-Al-Balad","Surah-Ash-Shams","Surah-Al-Lail","Surah-Adh-Dhuha","Surah-Al-Sharh","Surah-At-Tin","Surah-Al-Alaq","Surah-Al-Qadr","Surah-Al-Baiyina","Surah-Al-Zalzalah","Surah-Al-Adiyat","Surah-Al-Qari`a","Surah-At-Takathur","Surah-Al-Asr","Surah-Al-Humaza","Surah-Al-Fil","Surah-Quraish","Surah-Al-Ma`un","Surah-Al-Kauthar","Surah-Al-Kafirun","Surah-An-Nasr","Surah-Al-Lahab","Surah-Al-Ikhlas","Surah-Al-Falaq","Surah-Al-Nas"
    ]
}
    return JsonResponse({"surahList":res})

@csrf_exempt
def q_surah_audio(request,name):
    name=name.split('`')
    url = "https://online-quran-api.p.rapidapi.com/surahs/"
    for i in name:
        url+=i
    headers = {
        "X-RapidAPI-Key": "4120ca7630msh5566122415863dep16069fjsn207bd1f0e6f4",
        "X-RapidAPI-Host": "online-quran-api.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    return JsonResponse({"audio":response.json()['audio']})