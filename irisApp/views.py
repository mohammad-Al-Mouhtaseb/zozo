from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
import datetime ,json , pandas as pd
from experta import *
from users.views import *
from . models import *
import Notebooks.dep_bi as dep_bi
import Notebooks.panic as panic
import Notebooks.p_dep as p_dep

@csrf_exempt
def firstquiz(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        person_result=check_token(request)
        if check_token(request):
            a1=int(data['a1'])#Stress
            a2=int(data['a2'])#Anxiety
            a3=int(data['a3'])#Depression
            a4=int(data['a4'])#Stress
            a5=int(data['a5'])#Depression
            a6=int(data['a6'])#Anxiety
            a7=int(data['a7'])#Depression
            a8=int(data['a8'])#Anxiety

            patient=Patient.objects.get(email=person_result.email)
            iris=Iris.objects.update_or_create(Person_email=patient,das1=a1,das2=a2,das3=a3,das4=a4,das5=a5,das6=a6,das7=a7,das8=a8)
            iris=Iris.objects.get(Person_email=patient)
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
            

            # iris.das_d=True
            # iris.das_d=False
            # iris.das_d=False
            # iris.save()
            # return JsonResponse({'Depression':True,'Anxiety':False,'Stress':False}, status=200)


        else:
            return exp_logout(request)
    return JsonResponse({'state':'error request method'}, status=201)

panic_q_list=['Gender','Family_History','Personal_History','Current_Stressors','Symptoms','Severity','Impact_on_Life','Demographics','Medical_History','Psychiatric_History','Substance_Use','Coping_Mechanisms','Social_Support','Lifestyle_Factors']
Dep_Bi_q_list=['Sadness','Euphoric','Exhausted','Sleep_Dissorder','Mood_Swing','Suicidal_Thoughts','Anorxia','Authority_Respect','Try_Explanation','Aggressive_Response','Ignore_And_Move_On','Nervous_BreakDown','Admit_Mistakes','Overthinking','Sexual_Activity','Concentration','Optimisim']
P_Dep_q_list=['Gender','Age','Married','Number_Children','total_members','incoming_salary','incoming_business','incoming_no_business','labor_primary','Education_Level','gained_asset_Category','Durable_Asset_Category','Save_Asset_Category','Living_Expenses_Category','Other_Expenses_Category','Lasting_Investment_Category','No_Lasting_Investment_Category']

@csrf_exempt
def Panic(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        person_result=check_token(request)
        if check_token(request):
            try:
                patient = Patient.objects.get(email=person_result.email)
                Age = date.today().year - patient.birth.year
                Gender = "Male" if patient.gender == 'm' else "Female"
                data['Gender']=Gender
                new_test=[panic.mapping[data[key]] for key in panic_q_list]
                new_test.insert(0,Age)
                # pred = XGBoost.predict([new_test])[0]
                pred=panic.predict(new_test)[0]
                pred = False if pred == 0 else True
                fields = {'Person_email': patient, 'Positive_Negative_panic': pred}
                fields.update({key: data[key] for key in panic_q_list})
                Iris.objects.filter(Person_email=patient).update(**fields)
                return JsonResponse({'Iris_Panic' : pred}, status=200)
            except Exception as e:
                print(e)
                return JsonResponse({'state':'form is not valid','Exception':str(e)}, status=201)
        else:
            return exp_logout(request)
    return JsonResponse({'state':'error request method'}, status=201)

@csrf_exempt
def QPanic(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        person_result=check_token(request)
        if check_token(request):
            patient=Patient.objects.get(email=person_result.email)	
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
            answer=[["No","Yes"],["Yes","No"],["Moderate","High", "Low"],["Shortness of breath","Panic attacks","Chest pain","Dizziness", "Fear of losing control"],
                    ["Mild","Moderate", "Severe"],["Mild","Significant", "Moderate"],["Diabetes","Asthma", "None Demographics", "Heart disease"],
                    ["Rural","Urban"],["Bipolar disorder","Anxiety disorder", "Depressive disorder", "None Psychiatric History"],["None Substance Use","Drugs", "Alcohol"],
                    ["Socializing","Exercise", "Seeking therapy", "Meditation"],["High","Moderate", "Low"],["Sleep quality","Exercise", "Diet"]]
                
            try:
                obj_res=Iris.objects.filter(Person_email=patient)[0]
                all_q2=[obj_res.Family_History,obj_res.Personal_History,obj_res.Current_Stressors,obj_res.Symptoms,obj_res.Severity,obj_res.Impact_on_Life,obj_res.Demographics,obj_res.Medical_History,obj_res.Psychiatric_History,obj_res.Substance_Use,obj_res.Coping_Mechanisms,obj_res.Social_Support,obj_res.Lifestyle_Factors]
                if obj_res:
                    q=list()
                    j=0
                    for i in all_q2:
                        if i== None or i=="":
                            x={panic_q_list[j+1]:(questions[j],answer[j])}
                            q.append(x)
                        j+=1
                    return JsonResponse({'q':q}, status=200)
                else:
                    return JsonResponse({'q':panic_q_list[1::]}, status=200)
            except:
                q=list()
                j=0
                for i in panic_q_list[1::]:
                    x={i:(questions[j],answer[j])}
                    q.append(x)
                    j+=1
                return JsonResponse({'q':q}, status=200)
        else:
            return exp_logout(request)
    return JsonResponse({'state':'error request method'}, status=201)

@csrf_exempt
def Dep_Bi(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        person_result=check_token(request)
        if check_token(request):
            try:
                patient = Patient.objects.get(email=person_result.email)  
                new_test = {key:data[key] for key in Dep_Bi_q_list}
                new_test=pd.DataFrame(new_test, index=[0])
                pred=dep_bi.predict(new_test)
                if pred == 0:
                    pred="Bipolar Type-1"
                elif pred == 1:
                    pred="Bipolar Type-2"
                elif pred == 2:
                    pred="Depression"
                elif pred == 3:
                    pred="Normal"
                fields = {'Person_email': patient, 'Expert_Diagnose': pred}
                fields.update({key: data[key] for key in Dep_Bi_q_list})
                Iris.objects.filter(Person_email=patient).update(**fields)

                return JsonResponse({'Iris_Dep_Bi' : pred}, status=200)
            except Exception as e:
                print(e)
                return JsonResponse({'state':'form is not valid','Exception':str(e)}, status=201)
        else:
            return exp_logout(request)
    return JsonResponse({'state':'error request method'}, status=201)

@csrf_exempt
def QDep_Bi(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        person_result=check_token(request)
        if check_token(request):
            patient=Patient.objects.get(email=person_result.email)
            questions = [
                "Sadness?",
                "Euphoric?",
                "Exhausted?",
                "Sleep dissorder?",
                "Mood Swing?",
                "Suicidal thoughts?",
                "Anorxia?",
                "Authority Respect?",
                "Try-Explanation?",
                "Aggressive Response?",
                "Ignore & Move-On?",
                "Nervous Break-down?",
                "Admit_Mistakes?",
                "Overthinking?",
                "Sexual Activity?",
                "Concentration?",
                "Optimisim?"
            ]	
            answer=[["Usually","Sometimes","Seldom","Most-Often"],
                    ["Seldom","Most-Often","Usually","Sometimes"],
                    ["Sometimes","Usually","Seldom","Most-Often"],
                    ["Sometimes","Most-Often","Usually","Seldom"],
                    ["YES","NO"],["YES","NO"],["YES","NO"],["YES","NO"],["YES","NO"],
                    ["YES","NO"],["YES","NO"],["YES","NO"],["YES","NO"],["YES","NO"],
                    ["1 From 10","2 From 10","3 From 10","4 From 10","5 From 10","6 From 10","7 From 10","8 From 10","9 From 10","10 From 10"],
                    ["1 From 10","2 From 10","3 From 10","4 From 10","5 From 10","6 From 10","7 From 10","8 From 10","9 From 10","10 From 10"],
                    ["1 From 10","2 From 10","3 From 10","4 From 10","5 From 10","6 From 10","7 From 10","8 From 10","9 From 10","10 From 10"],
                    ]
            try:
                obj_res=Iris.objects.filter(Person_email=patient)[0]
                all_q2=[obj_res.Sadness,obj_res.Euphoric,obj_res.Exhausted,obj_res.Sleep_Dissorder,obj_res.Mood_Swing,obj_res.Suicidal_Thoughts,obj_res.Anorxia,obj_res.Authority_Respect,obj_res.Try_Explanation,obj_res.Aggressiv_Response,obj_res.Ignore_And_Move_On,obj_res.Nervous_BreakDown,obj_res.Admin_Mistakes,obj_res.Overthinking,obj_res.Sexual_Activity,obj_res.Concentration,obj_res.Optimisim,obj_res.Expert_Diagnose]
                if obj_res:
                    q=list()
                    j=0
                    for i in all_q2:
                        if i== None:
                            x={Dep_Bi_q_list[j]:(questions[j],answer[j])}
                            q.append(x)
                        j+=1
                    return JsonResponse({'q':q}, status=200)
                else:
                    return JsonResponse({'q':Dep_Bi_q_list}, status=200)
            except:
                q=list()
                j=0
                for i in Dep_Bi_q_list:
                    x={i:(questions[j],answer[j])}
                    q.append(x)
                    j+=1
                return JsonResponse({'q':q}, status=200)
        else:
            return exp_logout(request)
    return JsonResponse({'state':'error request method'}, status=201)

@csrf_exempt
def P_Dep(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        person_result=check_token(request)
        if check_token(request):
            try:
                patient = Patient.objects.get(email=person_result.email) 
                Age = date.today().year - patient.birth.year
                Gender = 1 if patient.gender == 'm' else 0 
                data['Gender']=Gender
                data["Age"]=Age
                new_test = [data[key] for key in P_Dep_q_list]
                pred=p_dep.predict(new_test)
                pred = "False" if pred == 0 else "True"
                fields = {'Person_email': patient, 'depressed': pred}
                int_list = [i for i in range(0, 100)]
                answer=[["Yes","No"],
                    int_list,
                    int_list,
                    int_list,
                    int_list,
                    int_list,
                    ["Yes","No"],['No Education', 'Primary', 'Secondary', 'High School', 'College'],
                    ['Very Low','Low','Medium', 'High', 'Very High'],
                    ['Very Low','Low','Low Medium', 'High Medium', 'High', 'Very High'],
                    ['Very Low','Low','Low Medium', 'High Medium', 'High', 'Very High'],
                    ['Very Low','Low','Low Medium', 'High Medium', 'High', 'Very High'],
                    ['Very Low','Low','Low Medium', 'High Medium', 'High', 'Very High'],
                    ['Very Low','Low','Low Medium', 'High Medium', 'High', 'Very High'],
                    ['Very Low','Low','Low Medium', 'High Medium', 'High', 'Very High']
                    ]  
                fields.update({key: answer[P_Dep_q_list.index(key)-2][data[key]] for key in P_Dep_q_list[2::]})
                Iris.objects.filter(Person_email=patient).update(**fields)
                return JsonResponse({'Iris_P_Dep' : pred}, status=200)
            except Exception as e:
                print(e)
                return JsonResponse({'state':'form is not valid','Exception':str(e)}, status=201)
        else:
            return exp_logout(request)
    return JsonResponse({'state':'error request method'}, status=201)

@csrf_exempt
def QP_Dep(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        person_result=check_token(request)
        if check_token(request):
            patient=Patient.objects.get(email=person_result.email)	
            questions = [
                "Married?",# ["Yes","No"]
                "Number_Children?",# n
                "total_members?",# n
                "incoming_salary?",# n
                "incoming_business?",# n
                "incoming_no_business?",# n
                "labor_primary?",# ["Yes","No"]
                "Education_Level?",#  ['No Education', 'Primary', 'Secondary', 'High School', 'College']
                "gained_asset_Category?",#5  ['Very Low','Low','Medium', 'High', 'Very High']
                "Durable_Asset_Category?",#6  ['Very Low','Low','Low Medium', 'High Medium', 'High', 'Very High']
                "Save_Asset_Category?",#6
                "Living_Expenses_Category?",#6
                "Other_Expenses_Category?",#6
                "Lasting_Investment_Category",#6
                "No_Lasting_Investment_Category"#6
            ]
            answer=[["Yes","No"],
                    [""],
                    [""],
                    [""],
                    [""],
                    [""],
                    ["Yes","No"],['No Education', 'Primary', 'Secondary', 'High School', 'College'],
                    ['Very Low','Low','Medium', 'High', 'Very High'],
                    ['Very Low','Low','Low Medium', 'High Medium', 'High', 'Very High'],
                    ['Very Low','Low','Low Medium', 'High Medium', 'High', 'Very High'],
                    ['Very Low','Low','Low Medium', 'High Medium', 'High', 'Very High'],
                    ['Very Low','Low','Low Medium', 'High Medium', 'High', 'Very High'],
                    ['Very Low','Low','Low Medium', 'High Medium', 'High', 'Very High'],
                    ['Very Low','Low','Low Medium', 'High Medium', 'High', 'Very High']
                    ]   
            try:
                obj_res=Iris.objects.filter(Person_email=patient)[0]
                all_q2=[obj_res.Married,obj_res.Number_Children,obj_res.total_members,obj_res.incoming_salary,obj_res.incoming_business,obj_res.incoming_no_business,obj_res.labor_primary,obj_res.Education_Level,obj_res.gained_asset_Category,obj_res.Durable_Asset_Category,obj_res.Save_Asset_Category,obj_res.Living_Expenses_Category,obj_res.Other_Expenses_Category,obj_res.Lasting_Investment_Category,obj_res.No_Lasting_Investment_Category]
                if obj_res:
                    q=list()
                    j=0
                    for i in all_q2:
                        if i== None or i=="":
                            x={P_Dep_q_list[j+2]:(questions[j],answer[j])}
                            q.append(x)
                        j+=1
                    return JsonResponse({'q':q}, status=200)
                else:
                    return JsonResponse({'q':P_Dep_q_list[2::]}, status=200)
            except:
                q=list()
                j=0
                for i in P_Dep_q_list[2::]:
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
        person_result=check_token(request)
        if check_token(request):
            try:
                p=Patient.objects.get(email=person_result.email)
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
        person_result=check_token(request)
        if check_token(request):
            if person_result.type=='doctor':
                patient_email=data['patient_email']
                try:
                    p=Patient.objects.get(email=patient_email)
                    info=Iris.objects.get(Person_email=p)
                except Exception as e:
                    print(e)
                    return JsonResponse({'state':'form is not valid'}, status=201)
                res=dict()
                for i in panic_q_list:
                    res[i]=getattr(info, i)
                return JsonResponse({"info":res}, status=201) 
            else:
                return JsonResponse({'state':'only doctor can view'}, status=201) 
        else:
            return exp_logout(request)
    return JsonResponse({'state':'error request method'}, status=201)

@csrf_exempt
def patient_list_for_doctor(request): #for doctor view Patient list
    if request.method == 'POST':
        data = json.loads(request.body)
        person_result=check_token(request)
        if check_token(request):
            try:
                users=Iris.objects.filter(Doctor_email=person_result)
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
