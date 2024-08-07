from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
import requests, json, threading
from . models import *
from django.core.files.base import ContentFile
from setting_apps.models import *
import base64
from pathlib import Path
import os

###################### Same code at server 2
# import scipy, torch
# from transformers import AutoProcessor, MusicgenForConditionalGeneration
# BASE_DIR = Path(__file__).resolve().parent.parent
# model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
# processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
# device = "cuda:0" if torch.cuda.is_available() else "cpu"
# model.to(device)
# sampling_rate = model.config.audio_encoder.sampling_rate

# @csrf_exempt
# def gen(request):data = json.loads(request.body)
    # desc=data['desc']
    # doctor=data['doctor']
    # patient=data['patient']
    # type=data['type']
    # wav_name="sounds/music/"+type+"/"+desc+".wav"
    # inputs = processor(
    #     text=[desc],
    #     padding=True,
    #     return_tensors="pt",
    # )
    # audio_values = model.generate(**inputs.to(device), do_sample=True, guidance_scale=3, max_new_tokens=1202)
    # scipy.io.wavfile.write(wav_name, rate=sampling_rate, data=audio_values[0, 0].cpu().numpy())
    # music=Music.objects.create(doctor=doctor,patient=patient,music_path=wav_name,type=type)
    # music.save()
    # return JsonResponse({"res":"sucsess"})

@csrf_exempt
def gen(request):
    data = json.loads(request.body)
    desc=data['desc']
    doctor=data['doctor']
    patient=data['patient']
    type=data['type']
    music_path="sounds/music/"+type+"_"+desc+".flac"
    key=Data.objects.get().Huggingface_API
    API_URL = "https://selene-flask.up.railway.app/music?desc="+desc+"&key="+key
    response = requests.get(API_URL)
    if response.status_code!=200:
        return JsonResponse({"res":"error at api"})
    fout = open('sounds/music/'+type+"_"+desc+".flac", 'wb+')
    for i in response:
        fout.write(i)
    fout.close()
    music=Music.objects.create(doctor=doctor,patient=patient,music_path=music_path,type=type)
    music.save()
    return JsonResponse({"res":"sucsess"})

@csrf_exempt
def get_music(request):
    data = json.loads(request.body)
    music_urls=data['url']
    try:
        m = open(music_urls, 'rb')
        response = FileResponse(m)
        return response
    except Exception as e:
        print(e)
        return JsonResponse({"res":None})

@csrf_exempt
def get_my_list(request):
    data = json.loads(request.body)
    user=data['user']
    m=None
    m=Music.objects.filter(patient=user)
    if len(m)==0:
        m=Music.objects.filter(doctor=user)

    music_urls=[]
    music_names=[]
    for i in m:
        music_urls.append(str(i.music_path))
        name=i.music_path.split('/')[-1].split(".")[0]
        music_names.append(name)
    return JsonResponse({"music_names":music_names,"music_urls":music_urls})

@csrf_exempt
def get_folder_list(request):
    data = json.loads(request.body)
    folder_name=data['folder_name']
    m=Music.objects.all()
    music_urls=[]
    music_names=[]
    for i in m: 
        n=i.music_path.split('/')[2].split('_')
        if n[0]==folder_name:
            music_urls.append(str(i.music_path))
            name=i.music_path.split('/')[-1].split(".")[0]
            music_names.append(name)
    return JsonResponse({"music_names":music_names,"music_urls":music_urls})

@csrf_exempt
def q_surahList(request):
    res={
    "surahList": [
        "Surah-Al-Fatihah","Surah-Al-Baqara","Surah-Al-Imran","Surah-An-Nisaa","Surah-Al-Maidah","Surah-Al-An`am","Surah-Al-A`raf","Surah-Al-Anfal","Surah-At-Taubah","Surah-Yunus","Surah-Hud","Surah-Yusuf","Surah-Ar-Ra`d","Surah-Ibrahim","Surah-Al-Hijr","Surah-An-Nahl","Surah-Israel","Surah-Al-Kahf","Surah-Maryam","Surah-Ta-ha","Surah-Al-Anbiyaa","Surah-Al-Hajj","Surah-Al-Muminun","Surah-An-Nur","Surah-Al-Furqan","Surah-Ash-Shu`araa","Surah-An-Naml","Surah-Al-Qasas","Surah-Al-Ankabut","Surah-Ar-Rum","Surah-Luqman","Surah-As-Sajda","Surah-Al-Ahzab","Surah-Saba","Surah-Fatir","Surah-Ya-Sin","Surah-As-Saffat","Surah-Sad","Surah-Az-Zumar","Surah-Al-Mu`min","Surah-Ha-Mim","Surah-Ash-Shura","Surah-Az-Zukhruf","Surah-Ad-Dukhan","Surah-Al-Jathiya","Surah-Al-Ahqaf","Surah-Muhammad","Surah-Al-Fat-h","Surah-Al-Hujurat","Surah-Qaf","Surah-Az-Zariyat","Surah-At-Tur","Surah-An-Najm","Surah-Al-Qamar","Surah-Ar-Rahman","Surah-Al-Waqi`a","Surah-Al-Hadid","Surah-Al-Mujadila","Surah-Al-Hashr","Surah-Al-Mumtahana","Surah-As-Saff","Surah-Al-Jumu`a","Surah-Al-Munafiqun","Surah-At-Tagabun","Surah-At-Talaq","Surah-At-Tahrim","Surah-Al-Mulk","Surah-Al-Qalam","Surah-Al-Haqqa","Surah-Al-Ma`arij","Surah-Nuh","Surah-Al-Jinn","Surah-Al-Muzzammil","Surah-Al-Muddathth","Surah-Al-Qiyamat","Surah-Ad-Dahr","Surah-Al-Mursalat","Surah-An-Nabaa","Surah-An-Nazi`at","Surah-Abasa","Surah-At-Takwir","Surah-Al-Infitar","Surah-Al-Mutaffife","Surah-Al-Inshiqaq","Surah-Al-Buruj","Surah-At-Tariq","Surah-Al-A`la","Surah-Al-Gashiya","Surah-Al-Fajr","Surah-Al-Balad","Surah-Ash-Shams","Surah-Al-Lail","Surah-Adh-Dhuha","Surah-Al-Sharh","Surah-At-Tin","Surah-Al-Alaq","Surah-Al-Qadr","Surah-Al-Baiyina","Surah-Al-Zalzalah","Surah-Al-Adiyat","Surah-Al-Qari`a","Surah-At-Takathur","Surah-Al-Asr","Surah-Al-Humaza","Surah-Al-Fil","Surah-Quraish","Surah-Al-Ma`un","Surah-Al-Kauthar","Surah-Al-Kafirun","Surah-An-Nasr","Surah-Al-Lahab","Surah-Al-Ikhlas","Surah-Al-Falaq","Surah-Al-Nas"
    ]
}
    return JsonResponse(res)

@csrf_exempt
def q_surah_audio(request,name):
    surahList= [
        "Surah-Al-Fatihah","Surah-Al-Baqara","Surah-Al-Imran","Surah-An-Nisaa","Surah-Al-Maidah","Surah-Al-An`am","Surah-Al-A`raf","Surah-Al-Anfal","Surah-At-Taubah","Surah-Yunus","Surah-Hud","Surah-Yusuf","Surah-Ar-Ra`d","Surah-Ibrahim","Surah-Al-Hijr","Surah-An-Nahl","Surah-Israel","Surah-Al-Kahf","Surah-Maryam","Surah-Ta-ha","Surah-Al-Anbiyaa","Surah-Al-Hajj","Surah-Al-Muminun","Surah-An-Nur","Surah-Al-Furqan","Surah-Ash-Shu`araa","Surah-An-Naml","Surah-Al-Qasas","Surah-Al-Ankabut","Surah-Ar-Rum","Surah-Luqman","Surah-As-Sajda","Surah-Al-Ahzab","Surah-Saba","Surah-Fatir","Surah-Ya-Sin","Surah-As-Saffat","Surah-Sad","Surah-Az-Zumar","Surah-Al-Mu`min","Surah-Ha-Mim","Surah-Ash-Shura","Surah-Az-Zukhruf","Surah-Ad-Dukhan","Surah-Al-Jathiya","Surah-Al-Ahqaf","Surah-Muhammad","Surah-Al-Fat-h","Surah-Al-Hujurat","Surah-Qaf","Surah-Az-Zariyat","Surah-At-Tur","Surah-An-Najm","Surah-Al-Qamar","Surah-Ar-Rahman","Surah-Al-Waqi`a","Surah-Al-Hadid","Surah-Al-Mujadila","Surah-Al-Hashr","Surah-Al-Mumtahana","Surah-As-Saff","Surah-Al-Jumu`a","Surah-Al-Munafiqun","Surah-At-Tagabun","Surah-At-Talaq","Surah-At-Tahrim","Surah-Al-Mulk","Surah-Al-Qalam","Surah-Al-Haqqa","Surah-Al-Ma`arij","Surah-Nuh","Surah-Al-Jinn","Surah-Al-Muzzammil","Surah-Al-Muddathth","Surah-Al-Qiyamat","Surah-Ad-Dahr","Surah-Al-Mursalat","Surah-An-Nabaa","Surah-An-Nazi`at","Surah-Abasa","Surah-At-Takwir","Surah-Al-Infitar","Surah-Al-Mutaffife","Surah-Al-Inshiqaq","Surah-Al-Buruj","Surah-At-Tariq","Surah-Al-A`la","Surah-Al-Gashiya","Surah-Al-Fajr","Surah-Al-Balad","Surah-Ash-Shams","Surah-Al-Lail","Surah-Adh-Dhuha","Surah-Al-Sharh","Surah-At-Tin","Surah-Al-Alaq","Surah-Al-Qadr","Surah-Al-Baiyina","Surah-Al-Zalzalah","Surah-Al-Adiyat","Surah-Al-Qari`a","Surah-At-Takathur","Surah-Al-Asr","Surah-Al-Humaza","Surah-Al-Fil","Surah-Quraish","Surah-Al-Ma`un","Surah-Al-Kauthar","Surah-Al-Kafirun","Surah-An-Nasr","Surah-Al-Lahab","Surah-Al-Ikhlas","Surah-Al-Falaq","Surah-Al-Nas"
    ]
    x=str(surahList.index(name)+1)
    if len(x)==1:
        return JsonResponse({"audio":"https://server8.mp3quran.net/afs/00"+x+".mp3"})
    if len(x)==2:
        return JsonResponse({"audio":"https://server8.mp3quran.net/afs/0"+x+".mp3"})
    if len(x)==3:
        return JsonResponse({"audio":"https://server8.mp3quran.net/afs/"+x+".mp3"})
