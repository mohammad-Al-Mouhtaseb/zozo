from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, FileResponse, HttpResponseRedirect
import requests

from transformers import pipeline
# import scipy

synthesiser = pipeline("text-to-audio", "facebook/musicgen-small")

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
    music = synthesiser(text, forward_params={"do_sample": True})
    # scipy.io.wavfile.write("musicgen_out.wav", rate=music["sampling_rate"], data=music["audio"])
    return HttpResponse(music["audio"], mimetype="audio/mpeg")
