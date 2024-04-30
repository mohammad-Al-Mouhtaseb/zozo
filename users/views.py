from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, FileResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
import string ,random,json
from django.contrib.auth.hashers import make_password
from . models import *
from chat.models import *
from django.contrib.auth import authenticate
import base64
from django.core.files.base import ContentFile
import requests
import base64
from cryptography.hazmat.primitives import asymmetric, serialization

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
        if chack_email(email):
            try:
                roll=data['type']
                if roll:
                    if roll=="doctor":
                        d=Doctor.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,country=country,gender=gender,birth=birth,type=roll)
                        d=Doctor.objects.get(email=email)
                        d.token= ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
                        d.save()
                        send_mail(email,"Welcome to selene..",{"email":email,"token":d.token})
                        generate_key_pair(email,2048)
                        return JsonResponse({'state':'success'}, status=200)
                    else:
                        roll="patient"
                        p=Patient.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,country=country,gender=gender,birth=birth,type=roll)
                        p=Patient.objects.get(email=email)
                        p.token= ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
                        p.save()
                        send_mail(email,"Welcome to selene..",{"email":email,"token":p.token})
                        generate_key_pair(email,2048)
                        return JsonResponse({'state':'success'}, status=200)      
                if roll==None:
                    roll="patient"
                    p=Patient.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,country=country,gender=gender,birth=birth,type=roll)
                    send_mail(email,"Welcome to selene..",None)
                    generate_key_pair(email,2048)
                    return JsonResponse({'state':'success'}, status=200)
            except Exception as e:
                return JsonResponse({'state':'Email already exists','Exception':str(e)}, status=201)
                print(e)
            return JsonResponse({'state':'form is not valid'}, status=201)
        return JsonResponse({'state':'email is not valid'}, status=201)
    return JsonResponse({'state':'error request method'}, status=201)

@csrf_exempt 
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email= data['email']
        password=data['password']
        try:
            user=User.objects.get(email=email)
            if user.is_active==True:
                if authenticate(request, email=email,password=password): 
                    if user.type=="patient":
                        Json_res=Patient.objects.get(email=email)
                        Json_res.token= ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
                        Json_res.save()
                        res=Patient.objects.filter(email=email).values()[0]
                        return JsonResponse({'state':{"first_name":res['first_name'],"last_name":res['last_name'],"email":res['email'],"country":res['country'],"gender":res['gender'],"birth":res['birth'],"photo":res['photo'],"language":res['language'],"password":"","token":res['token'],"type":res['type'],"private_key":res['private_key']}}, status=200)
                    else:
                        Json_res=Doctor.objects.get(email=email)
                        Json_res.token= ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
                        Json_res.save()
                        res=Doctor.objects.filter(email=email).values()[0]
                        return JsonResponse({'state':{"first_name":res['first_name'],"last_name":res['last_name'],"email":res['email'],"country":res['country'],"gender":res['gender'],"birth":res['birth'],"photo":res['photo'],"language":res['language'],"password":"","token":res['token'],"type":res['type'],"specialization":res['specialization'],"clinic_address":res['clinic_address'],"rate":res['rate'],"private_key":res['private_key']}}, status=200)

                return JsonResponse({'state':'form is not valid'}, status=201)
            else:
                return JsonResponse({'state':'Authenticate from email'}, status=201)
        except Exception as e:
            return JsonResponse({'state':'Email not found','Exception':str(e),'email':email}, status=201)
    return JsonResponse({'state':'error request method'}, status=201)

@csrf_exempt 
def logout(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email= data['email']
        token= data['token']
        obj_res=None
        try:
            obj_res=User.objects.get(email=email,token=token)
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
        email= data['email']
        obj_res=None
        try:
            obj_res=User.objects.get(email=email)
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
        email= data['email']
        token=data['token']
        params=data['params']
        new_values=data['new_values']
        user=User.objects.get(email=email,token=token)
        if user:
            if user.type=="patient":
                for i ,j in zip(params,new_values):
                    if hasattr(Patient, i):
                        try:
                            obj_res=Patient.objects.get(email=email)
                            if obj_res:
                                setattr(obj_res, i, j)
                                obj_res.save()
                                return JsonResponse({'state':"success"}, status=200)
                        except: 
                            return JsonResponse({'state':'form is not valid'}, status=201)       
            else:
                for i ,j in zip(params,new_values):
                    if hasattr(Doctor, i):
                        try:
                            obj_res=Doctor.objects.get(email=email)
                            if obj_res:
                                setattr(obj_res, i, j)
                                obj_res.save()
                                return JsonResponse({'state':"success"}, status=200)
                        except: 
                            return JsonResponse({'state':'form is not valid'}, status=201)
        return JsonResponse({'state':'form is not valid'}, status=201)
    return JsonResponse({'state':'error request method'}, status=201)

@csrf_exempt 
def photo(request,email):
    try:
        person=User.objects.get(email=email)
        img = open(str(person.photo), 'rb')
        response = FileResponse(img)
        return response
    except:
        return JsonResponse({"res":None})
    
@csrf_exempt 
def upload_photo(request,email):
    try:
        # data:image/jpeg;base64,
        data = json.loads(request.body)
        user= User.objects.get(email=email)
        format, imgstr = data["photo"].split(';base64,') 
        ext = format.split('/')[-1] 
        user.photo = ContentFile(base64.b64decode(imgstr), name=user.type+' '+user.first_name+' '+user.last_name+'.' + ext)
        user.save()
        return JsonResponse({'state':"success"}, status=200)
    except Exception as e:
        print(e)
        return JsonResponse({'state':str(e)}, status=201)

@csrf_exempt 
def get_profile(request,email):
    try:
        user=User.objects.get(email=email)
        if user.type=="patient":
            user=Patient.objects.get(email=email)
            return JsonResponse({"first_name":user.first_name,"last_name":user.last_name,"email":user.email,"birth":user.birth,"gender":user.gender})
        else:
            user=Doctor.objects.get(email=email)
            return JsonResponse({"first_name":user.first_name,"last_name":user.last_name,"email":user.email,"birth":user.birth,"gender":user.gender,"clinic_address":user.clinic_address,"rate":user.rate})
    except Exception as e:
        print(e)
        return JsonResponse({"user":None})
    
@csrf_exempt 
def check_token(request):
    data = json.loads(request.body)
    email= data['email']
    token= data['token']
    obj_res = User.objects.filter(email=email,token=token)
    if obj_res:
        return obj_res[0]
    else:
        return None
    
@csrf_exempt 
def get_doctor_list(request):
    res=[]
    try:
        users=Doctor.objects.all()
        # def myFunc(e):
        #     return e['rate']
        # users.sort(reverse=True,key=myFunc)
        userss = sorted(users, reverse=True)
        for i in users:
            res.append({"email":i.email,"first_name":i.first_name,"last_name":i.last_name,"specialization":i.specialization,"clinic_address":i.clinic_address,"rate":i.rate})
    except Exception as e:
        print(e)
        pass
    return JsonResponse({"doctors":res})

@csrf_exempt 
def reating(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        person_resul=check_token(request)
        if check_token(request):
            r=data['rate']
            doctor=data['doctor']
            doctor=Doctor.objects.get(email=doctor)
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


@csrf_exempt 
def send_mail(sendto,title,body):
    body="<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>Welcome to Selene</title><style>body { font-family: Arial, sans-serif; line-height: 1.6; }.container { width: 85%; margin: 17px auto; padding: 17px; }.header { background: #83c5be; padding: 5px 0; text-align: center; color: #fff; }.content { margin-top: 17px; }.footer { margin-top: 30px; text-align: center; color: #333; }</style></head><body><div class='container'><div class='header'><h1>Welcome to Selene!</h1> </div><div class='content'><p>Hello,<br>We're excited to have you on board. Selene is dedicated to supporting your mental health journey using the power of artificial intelligence.</p>With Selene, you can:<ul><li>Track your well-being through goal setting and to-do lists.</li><li>Enjoy music tailored by AI to fit your mood.</li><li>Connect with professionals for guidance and support.</li></ul><p>To get started, simply open the Selene app and explore the features designed to empower you every day.</p><p>You must authentication your email, to do that open this link: <a href='https://selene-m-h.up.railway.app/users/auth/"+body['email']+"/"+body['token']+"'> Authentication</a></p><p>If you have any questions or need assistance, our support team is here to help.</p><p>Warm regards,</p><p>The Selene Team</p></div><div class='footer'><p>© 2024 Selene. All rights reserved.</p></div></div></body></html>"
    payload = {
        "sendto": sendto,
        "name": "Selene",
        "replyTo": "",
        "ishtml": "true",
        "title": title,
        "body": body
    }
    
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "2e207fa9f9msha855123558f946dp1ec4f6jsn4ef4935f1378",
        "X-RapidAPI-Host": "rapidmail.p.rapidapi.com"
    }
    url = "https://rapidmail.p.rapidapi.com/"
    response = requests.post(url, json=payload, headers=headers)
    if(response.status_code!=200):
        headers= {
            "content-type": "application/json",
            "X-RapidAPI-Key": "2e207fa9f9msha855123558f946dp1ec4f6jsn4ef4935f1378",
            "X-RapidAPI-Host": "mail-sender-api1.p.rapidapi.com"
        }
        url = "https://mail-sender-api1.p.rapidapi.com/"
        response = requests.post(url, json=payload, headers=headers)

    print(response.json())

@csrf_exempt 
def chack_email(email):
    url = "https://validect-email-verification-v1.p.rapidapi.com/v1/verify"
    querystring = {"email":email}
    headers = {
        'X-RapidAPI-Key': '2e207fa9f9msha855123558f946dp1ec4f6jsn4ef4935f1378',
        'X-RapidAPI-Host': 'validect-email-verification-v1.p.rapidapi.com'
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code==200:
        v=response.json()['status']
        if v=="valid":
            # whats_for_dev(email)
            return True
    if int(str(email).split('@')[0])>200510000 and int(str(email).split('@')[0])<202511999 and str(email).split('@')[1]=="aiu.edu.sy":
        # whats_for_dev(email)
        return True
    return False

# @csrf_exempt 
# def whats_for_dev(email):
#     url = "https://whatsapp-messaging-hub.p.rapidapi.com/WhatsappSendMessage"
#     u=User.objects.get(email="m.almouhtaseb@gmail.com")
#     mhd_token=u.token
#     payload = {
#         "token": mhd_token,
#         "phone_number_or_group_id": "963941472414",
#         "is_group": False,
#         "message": "new registration: "+email,
#         "mentioned_ids": "",
#         "quoted_message_id": ""
#     }
#     headers = {
#         'content-type': 'application/json',
#         'X-RapidAPI-Key': '2e207fa9f9msha855123558f946dp1ec4f6jsn4ef4935f1378',
#         'X-RapidAPI-Host': 'whatsapp-messaging-hub.p.rapidapi.com'
#     }
#     response = requests.post(url, json=payload, headers=headers)

@csrf_exempt 
def auth(request,email,token):
    try:
        user=User.objects.get(email=email,token=token)
        user.is_active=True
        user.token=None
        user.save()
        return render(request,'auth.html')
    except:
        return HttpResponseForbidden(request)

@csrf_exempt 
def generate_key_pair(email,key_size):
    private_key = asymmetric.rsa.generate_private_key(
        public_exponent=65537,  # Common public exponent for RSA
        key_size=key_size
    )
    public_key = private_key.public_key()
    user=User.objects.get(email=email)
    user.private_key=private_key
    user.public_key=public_key
    user.save()