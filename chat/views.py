from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse, FileResponse
from users.views import *
from users.models import *
from .models import Message
import pusher, json, requests

# from langdetect import detect
# from googletrans import Translator
# from deep_translator import GoogleTranslator

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

                pusher_client.trigger("my-channel", 'my-event', {'sender':str(send),'message': msg})
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

