from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
import requests, json, threading
from . models import *
from django.core.files.base import ContentFile
import base64
from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent

# # Create your views here.

# import scipy, torch
# from transformers import AutoProcessor, MusicgenForConditionalGeneration
# model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
# processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
# device = "cuda:0" if torch.cuda.is_available() else "cpu"
# model.to(device)
# sampling_rate = model.config.audio_encoder.sampling_rate

@csrf_exempt
def gen_fun(request):
    data = json.loads(request.body)
    desc=data['desc']
    doctor=data['doctor']
    patient=data['patient']
    type=data['type']
    # flac_name="app/sounds/music/"+type+"/"+desc+".flac"
    # flac_name="/app/sounds/sss.flac"
    # wav_name="sounds/music/"+type+"/"+desc+".wav"

    # inputs = processor(
    #     text=[desc],
    #     padding=True,
    #     return_tensors="pt",
    # )
    # audio_values = model.generate(**inputs.to(device), do_sample=True, guidance_scale=3, max_new_tokens=1202)
    # scipy.io.wavfile.write(wav_name, rate=sampling_rate, data=audio_values[0, 0].cpu().numpy())
    try:
        API_URL = "https://api-inference.huggingface.co/models/facebook/musicgen-small"
        headers = {"Authorization": "Bearer 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"}
        audio_bytes = {
            "inputs": desc,
        }
        response = requests.post(API_URL, headers=headers, json=audio_bytes)
        # with open(flac_name, 'wb') as f:
        #     f.write(response.content)
        music=Music.objects.create(doctor=doctor,patient=patient,music=ContentFile(response.content, name=desc+'.flac'),type=type)
        music.save()
    except Exception as e:
        print(e)

@csrf_exempt
def gen(request):
    
    thread = threading.Thread(target=gen_fun(request))
    thread.start()

    return JsonResponse({"res":"sucsess"})

@csrf_exempt
def get_music(request):
    data = json.loads(request.body)
    music_urls=data['url']
    try:
        m = open(music_urls, 'rb')
        response = FileResponse(m)
        return response
    except:
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
        n=i.music_path.split('/')
        music_names.append(n[-1])
    return JsonResponse({"music_names":music_names,"music_urls":music_urls})

@csrf_exempt
def get_folder_list(request):
    data = json.loads(request.body)
    folder_name=data['folder_name']
    m=Music.objects.all()
    music_urls=[]
    music_names=[]
    for i in m:
        n=i.music_path.split('/')
        if n[2]==folder_name:
            music_urls.append(str(i.music_path))
            music_names.append(n[-1])
    return JsonResponse({"music_names":music_names,"music_urls":music_urls})

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
    return JsonResponse(res)

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
