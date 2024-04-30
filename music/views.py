from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, FileResponse, HttpResponseRedirect
import requests

# from transformers import pipeline
# # import scipy

# synthesiser = pipeline("text-to-audio", "facebook/musicgen-small")
from audiocraft.models import musicgen
from audiocraft.utils.notebook import display_audio
import torch
model = musicgen.MusicGen.get_pretrained('medium', device='cuda')
model.set_generation_params(duration=8)


# Create your views here.
def test(request,name):
    url = "https://spotify81.p.rapidapi.com/download_track"
    querystring = {"q":name,"onlyLinks":"1"}
    headers = {
        "X-RapidAPI-Key": "4120ca7630msh5566122415863dep16069fjsn207bd1f0e6f4",
        "X-RapidAPI-Host": "spotify81.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    print(response.json()[0]['url'])
    return HttpResponseRedirect(response.json()[0]['url'])

def create(request,text):
    res = model.generate([text], progress=True)
    display_audio(res, 32000)
    return HttpResponse(res, mimetype="audio/mpeg")
