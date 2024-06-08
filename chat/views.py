from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse, FileResponse
from users.views import *
from users.models import *
from .models import Message
import pusher, json, requests
import base64
from cryptography.hazmat.primitives import asymmetric, serialization

from langdetect import detect
from deep_translator import GoogleTranslator


@csrf_exempt
def chat_ai(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        text=data['text']
        url = "https://open-ai21.p.rapidapi.com/conversationpalm2"

        payload = { "messages": [
        		{
        			"role": "user",
        			"content": text
        		}
        	] }
        headers = {
        	"x-rapidapi-key": "4120ca7630msh5566122415863dep16069fjsn207bd1f0e6f4",
        	"x-rapidapi-host": "open-ai21.p.rapidapi.com",
        	"Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        return JsonResponse(response.json())
    return JsonResponse({'error':'error'},status=404)


@csrf_exempt
def translate(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        text=data['text']
        detected_language = detect(text)
        t_l=data['to']
        translated_text = GoogleTranslator(source=detected_language, target=t_l).translate(text)
        return JsonResponse({'translated':translated_text},status=200)
    return JsonResponse({'error':'error'},status=404)


@csrf_exempt 
def chat(request):  
    if request.method == 'POST':
        data = json.loads(request.body)
        person_resul=check_token(request)
        if check_token(request):
            send = data['email']
            recive = data['recive']
            try:
                msg = data['msg']
                # Create a new Message object and save it to the database
                message = Message(sender=User.objects.get(email=send), receiver=User.objects.get(email=recive), message=msg)
                message.save()
                
                pusher_client = pusher.Pusher(
                    app_id='1767996',
                    key='5571a7e3223bf9795d51',
                    secret='d5e835917dff91dd84ae',
                    cluster='ap2',
                    ssl=True
                )
                pusher_client.trigger(recive, 'event', {'sender':str(send),'message': msg})
                new_msg=Message.objects.create(sender=send,receiver=recive,message=msg).save()

            except:
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
                    res.append({"first_name":user.first_name,"last_name":user.last_name,"email":user.email,"birth":user.birth,"gender":user.gender,"clinic_address":user.clinic_address,"rate":user.rate})
            else:
                i_am = data['email']
                i_am=User.objects.get(email=i_am)
                users=Message.objects.filter(receiver=i_am)
                for i in users:
                    user=Patient.objects.filter(email=i.sender)[0]
                    res.append({"first_name":user.first_name,"last_name":user.last_name,"email":user.email,"birth":user.birth,"gender":user.gender})
            return JsonResponse({"network":res})
        else:
            return exp_logout(request)
    return JsonResponse({'state':'error request method'}, status=201)

@csrf_exempt
def note(request,channel):
    return render(request,'chat.html',{'channel':channel})
