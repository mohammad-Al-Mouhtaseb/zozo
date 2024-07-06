from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse, FileResponse
from users.views import *
from users.models import *
from irisApp.models import *
from .models import Message
import pusher, json, requests
import base64
from cryptography.hazmat.primitives import asymmetric, serialization

@csrf_exempt 
def chat(request):  
    if request.method == 'POST':
        data = json.loads(request.body)
        person_resul=check_token(request)
        if check_token(request):
            send = data['email']
            recive = data['recive']
            try:
                pusher_client = pusher.Pusher(
                    app_id='1767996',
                    key='5571a7e3223bf9795d51',
                    secret='d5e835917dff91dd84ae',
                    cluster='ap2',
                    ssl=True
                )
                msg = data['msg']
                if msg!="":
                    # Create a new Message object and save it to the database
                    message = Message(sender=User.objects.get(email=send), receiver=User.objects.get(email=recive), message=msg)
                    message.save()
                    pusher_client.trigger(recive, 'event', {'sender':str(send),'message': msg})
                else:
                    ms=[]
                    m1=Message.objects.filter(sender=User.objects.get(email=send),receiver=User.objects.get(email=recive))
                    m2=Message.objects.filter(sender=User.objects.get(email=recive),receiver=User.objects.get(email=send))
                    for i in m1:
                        ms.append({'sender': i.sender.email, 'message': i.message, 'timestamp': i.timestamp.strftime("%Y-%m-%d %H:%M:%S")})
                    for i in m2:
                        ms.append({'sender': i.sender.email, 'message': i.message, 'timestamp': i.timestamp.strftime("%Y-%m-%d %H:%M:%S")})

                    ms.sort(key=lambda x: x['timestamp'])

                    return JsonResponse({"send":send,"recive": recive,"ms":ms[-30:]})

            except Exception as e:
                pass
            ms=[]
            m1=Message.objects.filter(sender=User.objects.get(email=send),receiver=User.objects.get(email=recive))
            m2=Message.objects.filter(sender=User.objects.get(email=recive),receiver=User.objects.get(email=send))
            for i in m1:
                ms.append({'sender': i.sender.email, 'message': i.message, 'timestamp': i.timestamp.strftime("%Y-%m-%d %H:%M:%S")})
            for i in m2:
                ms.append({'sender': i.sender.email, 'message': i.message, 'timestamp': i.timestamp.strftime("%Y-%m-%d %H:%M:%S")})

            ms.sort(key=lambda x: x['timestamp'])

            return JsonResponse({"send":send,"recive": recive,"ms":ms[-30:]})
        else:
            return exp_logout(request)
    return JsonResponse({'state':'error request method'}, status=201)

@csrf_exempt 
def get_my_network(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        person_resul=check_token(request)
        if person_resul:
            res=[]
            if person_resul.type=='patient':
                doctor=Doctor.objects.all()
                for user in doctor:
                    res.append({"first_name":user.first_name,"last_name":user.last_name,"email":user.email,"birth":user.birth,"gender":user.gender,"clinic_address":user.clinic_address,"specialization":user.specialization,"rate":user.rate})
            else:
                i_am = data['email']
                i_am=User.objects.get(email=i_am)
                users=Iris.objects.filter(Doctor_email=i_am)
                for i in users:
                    user=Patient.objects.filter(email=i.Person_email)[0]
                    res.append({"first_name":user.first_name,"last_name":user.last_name,"email":user.email,"birth":user.birth,"gender":user.gender})
            return JsonResponse({"network":res})
        else:
            return exp_logout(request)
    return JsonResponse({'state':'error request method'}, status=201)