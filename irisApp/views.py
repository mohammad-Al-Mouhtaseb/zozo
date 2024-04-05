from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
import datetime ,json
from users.views import *
from . models import *
from joblib import load

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
                Age = date.today().year - person_resul.birth.year
                Gender = 1 if person_resul.gender == 'male' else 0 
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
                obj_res=Panic_Disorder.objects.filter(Person_Id=person_resul)
                fields = {
                    'Person_Id': person_resul,
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
                    obj_res = Panic_Disorder.objects.create(**fields)
                return JsonResponse({'Panic_Disorder' : pred}, status=200)

            except:
                params=dict(data)
                for k in params:
                    if k in all_q:
                        if hasattr(Panic_Disorder, k):
                            try:
                                obj=Panic_Disorder.objects
                                obj_res = obj.get(Person_Id=person_resul.id)
                                if obj_res:
                                    setattr(obj_res, k,params[k])
                                    obj_res.save()
                            except: 
                                return JsonResponse({'state':'form is not valid'}, status=201)
                obj=Panic_Disorder.objects.get(Person_Id=person_resul.id)
                Age = date.today().year - person_resul.birth.year
                Gender = 1 if person_resul.gender == 'male' else 0 
                new_test=[Age,Gender,obj.Family_History,obj.Personal_History,obj.Current_Stressors,obj.Symptoms,obj.Severity,obj.Impact_on_Life,obj.Demographics,obj.Medical_History,obj.Psychiatric_History,obj.Substance_Use,obj.Coping_Mechanisms,obj.Social_Support,obj.Lifestyle_Factors]
                pred=XGBoost.predict([new_test])
                if pred[0] == 0:
                    pred = False
                else :
                    pred = True

                return JsonResponse({'Panic_Disorder' : pred}, status=200)
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
                obj_res=Panic_Disorder.objects.filter(Person_Id=person_resul)[0]
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
def doctor_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        person_resul=check_token(request)
        if check_token(request):
            if person_resul.type=='doctor':
                p_id=data['p_id']
                try:
                    info=Panic_Disorder.objects.get(Person_Id=p_id)
                except:
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
def select_doctor(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        person_resul=check_token(request)
        if check_token(request):
            try:
                obj_res = Panic_Disorder.objects.get(Person_Id=person_resul.id)
                if obj_res:
                    selection=data['doctor']
                    doc=Doctor.objects.get(id=selection)
                    setattr(obj_res, "Doctor_Id", doc)
                    obj_res.save()
                    return JsonResponse({'state':'success'}, status=200)
                elif Patient.objects.get(Person_Id=person_resul.id):
                    return JsonResponse({'state':'you must doing test'}, status=201)
            except: 
                return JsonResponse({'state':'form is not valid'}, status=201)  
            
        else:
            return exp_logout(request)
    return JsonResponse({'state':'error request method'}, status=201)
