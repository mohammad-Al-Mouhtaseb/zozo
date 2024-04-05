from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
import string ,random,json
from django.contrib.auth.hashers import make_password
from . models import *
from django.contrib.auth import authenticate

# Create your views here.

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        first_name=data['first_name']
        last_name=data['last_name']
        email=data['email']
        password=data['password']
        country=data['country']
        gender=data['gender']
        birth=data['birth']
        roll=None
        try:
            roll=data['type']
            if roll:
                if roll=="doctor":
                    d=Doctor.objects.create_user(first_name=first_name,last_name=last_name,username=email,email=email,password=password,country=country,gender=gender,birth=birth,type=roll)
                    return JsonResponse({'state':'success'}, status=200)
                else:
                    roll="patient"
                    p=Patient.objects.create_user(first_name=first_name,last_name=last_name,username=email,email=email,password=password,country=country,gender=gender,birth=birth,type=roll)
                    return JsonResponse({'state':'success'}, status=200)      
        except Exception as e:
            print(e)
        if roll==None:
            roll="patient"
            p=Patient.objects.create_user(first_name=first_name,last_name=last_name,username=email,email=email,password=password,country=country,gender=gender,birth=birth,type=roll)
            return JsonResponse({'state':'success'}, status=200)
        return JsonResponse({'state':'form is not valid'}, status=201)
    return JsonResponse({'state':'error request method'}, status=201)

@csrf_exempt 
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email= data['email']
        password=data['password']
        if authenticate(request, username=email,password=password):
            Json_res=Abo.objects.get(email=email)
            Json_res.token= ''.join(random.choices(string.ascii_uppercase + string.digits, k=50))
            Json_res.save()
            try:
                res=Patient.objects.filter(email=email).values()[0]
                return JsonResponse({'state':{"id":res['id'],"first_name":res['first_name'],"last_name":res['last_name'],"email":res['email'],"country":res['country'],"gender":res['gender'],"birth":res['birth'],"photo":res['photo'],"language":res['language'],"password":"","token":res['token'],"type":res['type']}}, status=200)
            except Exception as e:
                print('1')
                print(e)
            try:
                res=Doctor.objects.filter(email=email).values()[0]
                return JsonResponse({'state':{"id":res['id'],"first_name":res['first_name'],"last_name":res['last_name'],"email":res['email'],"country":res['country'],"gender":res['gender'],"birth":res['birth'],"photo":res['photo'],"language":res['language'],"password":"","token":res['token'],"type":res['type']}}, status=200)
            except Exception as e:
                print('2')
                print(e)
        return JsonResponse({'state':'form is not valid'}, status=201)
    return JsonResponse({'state':'error request method'}, status=201)

@csrf_exempt 
def logout(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id= data['id']
        token= data['token']
        obj_res=None
        try:
            obj_res=Abo.objects.get(id=id,token=token)
        except:
            pass
        if obj_res!=None:
            obj_res.token= None
            obj_res.save()
            return JsonResponse({'user':'logout'}, status=200)
        return JsonResponse({'state':'form is not valid'}, status=201)
    return JsonResponse({'state':'error request method'}, status=201)

@csrf_exempt 
def exp_logout(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id= data['id']
        obj_res=None
        try:
            obj_res=Abo.objects.get(id=id)
        except:
            pass
        if obj_res:
            obj_res.token= None
            obj_res.save()
            return JsonResponse({'user':'logout'}, status=200)
        return JsonResponse({'state':'form is not valid'}, status=201)
    return JsonResponse({'state':'error request method'}, status=201)

@csrf_exempt 
def edit(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id= data['id']
        token=data['token']
        param=data['param']
        new_value=data['new_value']
        person_obj=Abo.objects.get(id=id,token=token)
        if person_obj:
            if person_obj.type=="patient":
                if hasattr(Patient, param):
                    try:
                        obj_res=Patient.objects.get(id=id)
                        if obj_res:
                            setattr(obj_res, param, new_value)
                            obj_res.save()
                            return JsonResponse({'state':"success"}, status=200)
                    except: 
                        return JsonResponse({'state':'form is not valid'}, status=201)       
            elif person_obj.type=="doctor":
                if hasattr(Doctor, param):
                    try:
                        obj_res=Doctor.objects.get(id=id)
                        if obj_res:
                            setattr(obj_res, param, new_value)
                            obj_res.save()
                            return JsonResponse({'state':"success"}, status=200)
                    except: 
                        return JsonResponse({'state':'form is not valid'}, status=201)
        return JsonResponse({'state':'form is not valid'}, status=201)
    return JsonResponse({'state':'error request method'}, status=201)

@csrf_exempt 
def photo(request,id):
    try:
        person=Abo.objects.get(id=id)
        img = open(str(person.photo), 'rb')
        response = FileResponse(img)
        return response
    except:
        return JsonResponse({"res":None})
    
@csrf_exempt 
def get_profile(request,id):
    try:
        res=Abo.objects.get(id=id)
        if res.type=="patient":
            res=Patient.objects.get(id=id)
            return JsonResponse({"first_name":res.first_name,"last_name":res.last_name,"email":res.email,"birth":res.birth,"gender":res.gender})
        else:
            res=Doctor.objects.get(id=id)
            return JsonResponse({"first_name":res.first_name,"last_name":res.last_name,"email":res.email,"birth":res.birth,"gender":res.gender,"clinic_address":res.clinic_address,"rate":res.rate})
    except Exception as e:
        print(e)
        return JsonResponse({"res":None})
    
@csrf_exempt 
def check_token(request):
    data = json.loads(request.body)
    id= data['id']
    token= data['token']
    obj_res = Abo.objects.filter(id=id,token=token)
    if obj_res:
        return obj_res[0]
    else:
        return None
    
@csrf_exempt 
def get_doctor_list(request):
    res=[]
    users=Doctor.objects.filter(type='doctor')
    for i in users:
        res.append({"id":i.id,"first_name":i.first_name,"last_name":i.last_name,"rate":i.rate})
    return JsonResponse({"network":res})

@csrf_exempt 
def reating(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        person_resul=check_token(request)
        if check_token(request):
            r=data['rate']
            doctor=data['doctor']
            doctor=Doctor.objects.get(id=doctor)
            old_r=doctor.rate
            old_num_rating=doctor.num_of_rate
            new_rate=(old_r+r)/(old_num_rating+1)
            new_num_rating=old_num_rating+1
            doctor.rate=new_rate
            doctor.num_of_rate=new_num_rating
            doctor.save()
            return JsonResponse({'new_rate':new_rate}, status=200)
        else:
            return exp_logout(request)
    return JsonResponse({'state':'error request method'}, status=201)