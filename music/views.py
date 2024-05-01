from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, FileResponse, HttpResponseRedirect
import requests

from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy

# model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
# processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
# import torch
# device = "cuda:0" if torch.cuda.is_available() else "cpu"
# device="cpu"
# model.to(device)
# sampling_rate = model.config.audio_encoder.sampling_rate


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
    # inputs = processor(
    #     text=[text],
    #     padding=True,
    #     return_tensors="pt",
    # )
    # audio_values = model.generate(**inputs.to(device), do_sample=True, guidance_scale=3, max_new_tokens=256)
    # scipy.io.wavfile.write("musicgen_out.wav", rate=sampling_rate, data=audio_values)

    # return HttpResponse(sampling_rate) 
    pass
