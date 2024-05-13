from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
import datetime ,json
from experta import *
from users.views import *
from . models import *
from joblib import load

@csrf_exempt
def firstquiz(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        person_resul=check_token(request)
        if check_token(request):
            a1=int(data['a1'])#Stress
            a2=int(data['a2'])#Anxiety
            a3=int(data['a3'])#Depression
            a4=int(data['a4'])#Stress
            a5=int(data['a5'])#Depression
            a6=int(data['a6'])#Anxiety
            a7=int(data['a7'])#Depression
            a8=int(data['a8'])#Anxiety
            
            iris=Iris.objects.create(das1=a1,das2=a2,das3=a3,das4=a4,das5=a5,das6=a6,das7=a7,das8=a8)

            class Robot(KnowledgeEngine):
                @Rule(NOT(Fact(Depression=W())))
                def Depression(self):
                    self.declare(Fact(Depression=bool((a3+a5+a7)>=4)))

                @Rule((Fact(Depression=W())) and (NOT(Fact(Anxiety=W()))))
                def Anxiety(self):
                    self.declare(Fact(Anxiety=bool((a2+a6+a8)>=4)))

                @Rule((Fact(Anxiety=W())) and (NOT(Fact(Stress=W()))))
                def Stress(self):
                    self.declare(Fact(Stress=bool((a1+a4)>=3)))
                    
            engine = Robot()
            engine.reset()
            engine.run()
            facts=list(engine.facts.items())
            d=str(facts[1])
            a=str(facts[2])
            s=str(facts[3])
            d=d[9:len(d)-2]
            a=a[9:len(a)-2]
            s=s[9:len(s)-2]
            d=d.split('=')
            a=a.split('=')
            s=s.split('=')
            if(d[1]=="True"):
                a[1]="False"
                s[1]="False"
                iris.das_d=True
            elif(a[1]=="True"):
                s[1]="False"
                iris.das_a=True
            elif(s[1]=="True"):
                iris.das_s=True
            iris.save()
            return JsonResponse({d[0]:d[1],a[0]:a[1],s[0]:s[1]}, status=200)
        else:
            return exp_logout(request)
    return JsonResponse({'state':'error request method'}, status=201)


all_q=['Family_History','Personal_History','Current_Stressors','Symptoms','Severity','Impact_on_Life','Demographics','Medical_History','Psychiatric_History','Substance_Use','Coping_Mechanisms','Social_Support','Lifestyle_Factors']

@csrf_exempt
def Panic(request):
    mapping= load('./savedModels/mapping.joblib')
    XGBoost= load('./savedModels/XGBoost.joblib')
    
    if request.method == 'POST':
        data = json.loads(request.body)
        person_resul=check_token(request)
        if check_token(request):
            try:
                patient=Patient.objects.get(email=person_resul
                                            .email)
                Age = date.today().year - patient.birth.year
                Gender = 1 if patient.gender == 'male' else 0 
                Family_History=data['Family_History']	
                Personal_History=data['Personal_History']	
                Current_Stressors=data['Current_Stressors']	
                Symptoms=data['Symptoms']	
                Severity=data['Severity']	
                Impact_on_Life=data['Impact_on_Life']	
                Demographics=data['Demographics']	
                Medical_History=data['Medical_History']	
                Psychiatric_History=data['Psychiatric_History']	
                Substance_Use=data['Substance_Use']	
                Coping_Mechanisms=data['Coping_Mechanisms']	
                Social_Support=data['Social_Support']	
                Lifestyle_Factors=data['Lifestyle_Factors']	

                new_test=[Age,Gender,Family_History,Personal_History,Current_Stressors,Symptoms,Severity,Impact_on_Life,Demographics,Medical_History,Psychiatric_History,Substance_Use,Coping_Mechanisms,Social_Support,Lifestyle_Factors]
                pred=XGBoost.predict([new_test])
                pred= False if pred[0] == 0 else True
                obj_res=Iris.objects.filter(Person_email=patient)
                fields = {
                    'Person_email': patient,
                    'Positive_Negative': pred,
                    'Family_History': Family_History,
                    'Personal_History': Personal_History,
                    'Current_Stressors': Current_Stressors,
                    'Symptoms': Symptoms,
                    'Severity': Severity,
                    'Impact_on_Life': Impact_on_Life,
                    'Demographics': Demographics,
                    'Medical_History': Medical_History,
                    'Psychiatric_History': Psychiatric_History,
                    'Substance_Use': Substance_Use,
                    'Coping_Mechanisms': Coping_Mechanisms,
                    'Social_Support': Social_Support,
                    'Lifestyle_Factors': Lifestyle_Factors
                }
                if obj_res:
                    obj_res.update(**fields)
                else:
                    obj_res = Iris.objects.create(**fields)
                return JsonResponse({'Iris' : pred}, status=200)

            except Exception as e:
                params=dict(data)
                for k in params:
                    if k in all_q:
                        if hasattr(Iris, k):
                            try:
                                obj_res=Iris.objects.get(Person_email=patient)
                                if obj_res:
                                    setattr(obj_res, k,params[k])
                                    obj_res.save()
                            except Exception as e:
                                return JsonResponse({'state':'form is not valid'}, status=201)
                obj=Iris.objects.get(Person_email=patient.email)
                Age = date.today().year - patient.birth.year
                Gender = 1 if patient.gender == 'male' else 0 
                new_test=[Age,Gender,obj.Family_History,obj.Personal_History,obj.Current_Stressors,obj.Symptoms,obj.Severity,obj.Impact_on_Life,obj.Demographics,obj.Medical_History,obj.Psychiatric_History,obj.Substance_Use,obj.Coping_Mechanisms,obj.Social_Support,obj.Lifestyle_Factors]
                pred=XGBoost.predict([new_test])
                if pred[0] == 0:
                    pred = False
                else :
                    pred = True

                return JsonResponse({'Iris' : pred}, status=200)
            return JsonResponse({'state':'form is not valid'}, status=201)
        else:
            return exp_logout(request)
    return JsonResponse({'state':'error request method'}, status=201)

@csrf_exempt
def QPanic(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        person_resul=check_token(request)
        if check_token(request):
            patient=Patient.objects.get(email=person_resul
                                            .email)
            questions = [
            "Do you have a family history of any medical conditions?",
            "Do you have a personal history of any medical conditions?",
            "How would you rate your current stress levels?",
            "What symptoms have you been experiencing recently?",
            "On a scale of 0-2, how would you rate the severity of your symptoms?",
            "How have these symptoms impacted your daily life?",
            "Could you provide some demographic information?",
            "What is your general medical history?",
            "Do you have a history of psychiatric conditions?",
            "Have you used any substances? If so, which ones?",
            "What coping mechanisms do you use to manage stress?",
            "What kind of social support do you have?",
            "Are there any lifestyle factors that might be affecting your health?",
        ]
            answer=[["No","Yes"],["Yes","No"],["Moderate","High", "2 for Low"],["Shortness of breath","Panic attacks","2 for Chest pain","3 for Dizziness", "4 for Fear of losing control"],
                    ["Mild","Moderate", "2 for Severe"],["Mild","Significant", "2 for Moderate"],["Diabetes","Asthma", "2 for None", "3 for Heart disease"],
                    ["Rural","Urban"],["Bipolar disorder","Anxiety disorder", "2 for Depressive disorder", "3 for None"],["None","Drugs", "2 for Alcohol"],
                    ["Socializing","Exercise", "2 for Seeking therapy", "3 for Meditation"],["High","Moderate", "2 for Low"],["Sleep quality","Exercise", "2 for Diet"]]
            try:
                obj_res=Iris.objects.filter(Person_email=patient)[0]
                all_q2=[obj_res.Family_History,obj_res.Personal_History,obj_res.Current_Stressors,obj_res.Symptoms,obj_res.Severity,obj_res.Impact_on_Life,obj_res.Demographics,obj_res.Medical_History,obj_res.Psychiatric_History,obj_res.Substance_Use,obj_res.Coping_Mechanisms,obj_res.Social_Support,obj_res.Lifestyle_Factors]
                if obj_res:
                    q=list()
                    j=0
                    for i in all_q2:
                        if i== None:
                            x={all_q[j]:(questions[j],answer[j])}
                            q.append(x)
                        j+=1
                    return JsonResponse({'q':q}, status=200)
                else:
                    return JsonResponse({'q':all_q}, status=200)
            except:
                q=list()
                j=0
                for i in all_q:
                    x={i:(questions[j],answer[j])}
                    q.append(x)
                    j+=1
                return JsonResponse({'q':q}, status=200)
        else:
            return exp_logout(request)
    return JsonResponse({'state':'error request method'}, status=201)

@csrf_exempt
def select_doctor(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        person_resul=check_token(request)
        if check_token(request):
            try:
                p=Patient.objects.get(email=person_resul.email)
                obj_res = Iris.objects.filter(Person_email=p)
                if len(obj_res)!=0:
                    selection=data['doctor']
                    doc=Doctor.objects.get(email=selection)
                    setattr(obj_res, "Doctor_email", doc)
                    obj_res.save()
                    return JsonResponse({'state':'success'}, status=200)
                else:
                    return JsonResponse({'state':'you must doing test'}, status=201)
            except Exception as e: 
                print(e)
                return JsonResponse({'state':'form is not valid'}, status=201)  
            
        else:
            return exp_logout(request)
    return JsonResponse({'state':'error request method'}, status=201)

@csrf_exempt
def doctor_view(request): #for doctor view Patient data
    if request.method == 'POST':
        data = json.loads(request.body)
        person_resul=check_token(request)
        if check_token(request):
            if person_resul.type=='doctor':
                patient_email=data['patient_email']
                try:
                    p=Patient.objects.get(email=patient_email)
                    info=Iris.objects.get(Person_email=p)
                except Exception as e:
                    print(e)
                    return JsonResponse({'state':'form is not valid'}, status=201)
                res=dict()
                for i in all_q:
                    res[i]=getattr(info, i)
                return JsonResponse({"info":res}, status=201) 
            else:
                return JsonResponse({'state':'only doctor can view'}, status=201) 
        else:
            return exp_logout(request)
    return JsonResponse({'state':'error request method'}, status=201)

@csrf_exempt
def patient_list_for_doctor(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        person_resul=check_token(request)
        if check_token(request):
            try:
                users=Iris.objects.filter(Doctor_email=person_resul)
                res=[]
                for i in users:
                    u=Patient.objects.get(email=i.Person_email)
                    res.append({"email":u.email,"first_name":u.first_name,"last_name":u.last_name})
                return JsonResponse({'info':res}, status=200)  
            except Exception as e: 
                print(e)
                return JsonResponse({'state':'form is not valid'}, status=201)  
        else:
            return exp_logout(request)
    return JsonResponse({'state':'error request method'}, status=201)
