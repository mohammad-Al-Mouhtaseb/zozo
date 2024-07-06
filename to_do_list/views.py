from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse, FileResponse
from users.views import *
from users.models import *
from . models import *
from . forms import *

@csrf_exempt
def set_to_do_list(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        person_resul=check_token(request)
        if check_token(request):
            email= data['email']
            try:
                if person_resul.type=="doctor":
                    patients= data['patients']
                    aim= data['aim']
                    goals=data['goals']
                    for i in patients:
                        for j in goals:
                            p=Patient.objects.get(email=i)
                            form = add_goal({'doctor':person_resul,'patient':p,'aim':aim,'goal':j})
                            if form.is_valid():
                                form.save()
                    return JsonResponse({'state':"success"}, status=200)
            except Exception as e:
                print(e)
            return JsonResponse({'state':'form is not valid'}, status=201)
        else:
            return exp_logout(request)
    return JsonResponse({'state':'error request method'}, status=201)

@csrf_exempt
def get_to_do_list(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        person_resul=check_token(request)
        if check_token(request):
            email= data['email']
            try:
                user=User.objects.get(email=email)
                res=To_Do.objects.filter(patient=user)
                x=dict()
                for i in res:
                    k=i.aim
                    v={i.goal:True}
                    if k in x:
                        x[k].append(v)
                    else:
                        x[k]=[v]
                return JsonResponse({'state':x}, status=200)
            except Exception as  e:
                print(e)
            return JsonResponse({'state':'form is not valid'}, status=201)
        else:
            return exp_logout(request)
    return JsonResponse({'state':'error request method'}, status=201)
