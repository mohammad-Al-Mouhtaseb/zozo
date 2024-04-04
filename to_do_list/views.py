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
            id= data['id']
            try:
                if person_resul.type=="doctor":
                    patients= data['patients']
                    aim= data['aim']
                    goals=data['goals']
                    for i in patients:
                        for j in goals:
                            form = add_goal({'doctor':id,'patient':i,'aim':aim,'goal':j})
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
            id= data['id']
            try:
                res=To_Do.objects.filter(patient=id)
                x=dict()
                for i in res:
                    k=i.aim
                    v={i.goal:i.is_done}
                    if k in x:
                        x[k].append(v)
                    else:
                        x[k]=[v]
                return JsonResponse({'state':x}, status=200)
            except:
                pass
            return JsonResponse({'state':'form is not valid'}, status=201)
        else:
            return exp_logout(request)
    return JsonResponse({'state':'error request method'}, status=201)

@csrf_exempt
def done_to_do_goal(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        person_resul=check_token(request)
        if check_token(request):
            id= data['id']
            aim=data['aim']
            goal=data['goal']
            try:
                res=To_Do.objects.get(patient=id,aim=aim,goal=goal)
                print(res)
                if res:
                    setattr(res, 'is_done', True)
                    res.save()
                return JsonResponse({'state':"success"}, status=200)
            except:
                pass
            return JsonResponse({'state':'form is not valid'}, status=201)
        else:
            return exp_logout(request)
    return JsonResponse({'state':'error request method'}, status=201)