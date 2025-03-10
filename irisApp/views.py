from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
import datetime ,json , pandas as pd, Notebooks.dep_bi as dep_bi, Notebooks.panic as panic, Notebooks.p_dep as p_dep
# from experta import *
from users.views import *
from . models import *

panic_q_list=['Gender','Family_History','Personal_History','Current_Stressors','Symptoms','Severity','Impact_on_Life','Demographics','Medical_History','Psychiatric_History','Substance_Use','Coping_Mechanisms','Social_Support','Lifestyle_Factors']
Dep_Bi_q_list=['Sadness','Euphoric','Exhausted','Sleep_Dissorder','Mood_Swing','Suicidal_Thoughts','Anorxia','Authority_Respect','Try_Explanation','Aggressive_Response','Ignore_And_Move_On','Nervous_BreakDown','Admit_Mistakes','Overthinking','Sexual_Activity','Concentration','Optimisim']
P_Dep_q_list=['Gender','Age','Married','Number_Children','total_members','incoming_salary','incoming_business','incoming_no_business','labor_primary','Education_Level','gained_asset_Category','Durable_Asset_Category','Save_Asset_Category','Living_Expenses_Category','Other_Expenses_Category','Lasting_Investment_Category','No_Lasting_Investment_Category']

@csrf_exempt
def firstquiz(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        person_result=check_token(request)
        if check_token(request):
            a1=data['a1']#Stress
            a2=data['a2']#Anxiety
            a3=data['a3']#Depression
            a4=data['a4']#Stress
            a5=data['a5']#Depression
            a6=data['a6']#Anxiety
            a7=data['a7']#Depression
            a8=data['a8']#Anxiety
            
            ###################### Same code at server 3
            # patient=Patient.objects.get(email=person_result.email)
            # iris=Iris.objects.update_or_create(Person_email=patient,das1=a1,das2=a2,das3=a3,das4=a4,das5=a5,das6=a6,das7=a7,das8=a8)
            # iris=Iris.objects.get(Person_email=patient)
            # class Robot(KnowledgeEngine):
            #     @Rule(NOT(Fact(Depression=W())))
            #     def Depression(self):
            #         self.declare(Fact(Depression=bool((a3+a5+a7)>=4)))

            #     @Rule((Fact(Depression=W())) and (NOT(Fact(Anxiety=W()))))
            #     def Anxiety(self):
            #         self.declare(Fact(Anxiety=bool((a2+a6+a8)>=4)))

            #     @Rule((Fact(Anxiety=W())) and (NOT(Fact(Stress=W()))))
            #     def Stress(self):
            #         self.declare(Fact(Stress=bool((a1+a4)>=3)))
                    
            # engine = Robot()
            # engine.reset()
            # engine.run()
            # facts=list(engine.facts.items())
            # d=str(facts[1])
            # a=str(facts[2])
            # s=str(facts[3])
            # d=d[9:len(d)-2]
            # a=a[9:len(a)-2]
            # s=s[9:len(s)-2]
            # d=d.split('=')
            # a=a.split('=')
            # s=s.split('=')
            # if(d[1]=="True"):
            #     a[1]="False"
            #     s[1]="False"
            #     iris.das_d=True
            # elif(a[1]=="True"):
            #     s[1]="False"
            #     iris.das_a=True
            # elif(s[1]=="True"):
            #     iris.das_s=True
            # iris.save()
            # return JsonResponse({d[0]:d[1],a[0]:a[1],s[0]:s[1]}, status=200)
            API_URL = "https://selene-flask.up.railway.app/expert?a1="+a1+"&a2="+a2+"&a3="+a3+"&a4="+a4+"&a5="+a5+"&a6="+a6+"&a7="+a7+"&a8="+a8
            response = requests.get(API_URL)
            if response.status_code!=200:
                return JsonResponse({"res":"error at api"}, status=201)
            else:
                response_json = response.json()
                patient=Patient.objects.get(email=person_result.email)
                Age = date.today().year - patient.birth.year
                Gender = "Male" if patient.gender == 'm' else "Female"
                last_doctor=None
                try:
                    iris=Iris.objects.get(Person_email=patient)
                    if response_json['Anxiety']:
                        iris.Family_History=None
                        iris.Personal_History=None
                        iris.Current_Stressors=None
                        iris.Symptoms=None
                        iris.Severity=None
                        iris.Impact_on_Life=None
                        iris.Demographics=None
                        iris.Medical_History=None
                        iris.Psychiatric_History=None
                        iris.Substance_Use=None
                        iris.Coping_Mechanisms=None
                        iris.Social_Support=None
                        iris.Lifestyle_Factors=None
                        iris.Positive_Negative_panic=None
                    elif response_json['Stress']:
                        iris.Sadness = None
                        iris.Euphoric = None
                        iris.Exhausted = None
                        iris.Sleep_Dissorder = None
                        iris.Mood_Swing = None
                        iris.Suicidal_Thoughts = None
                        iris.Anorxia = None
                        iris.Authority_Respect = None
                        iris.Try_Explanation = None
                        iris.Aggressive_Response = None
                        iris.Ignore_And_Move_On = None
                        iris.Nervous_BreakDown = None
                        iris.Admit_Mistakes = None
                        iris.Overthinking = None
                        iris.Sexual_Activity = None
                        iris.Concentration = None
                        iris.Optimisim = None
                        iris.Expert_Diagnose = None
                    elif response_json['Depression']:
                        iris.Married = None
                        iris.Number_Children = None
                        iris.total_members = None
                        iris.incoming_salary = None
                        iris.incoming_business = None
                        iris.incoming_no_business = None
                        iris.labor_primary = None
                        iris.Education_Level = None
                        iris.gained_asset_Category = None
                        iris.Durable_Asset_Category = None
                        iris.Save_Asset_Category = None
                        iris.Living_Expenses_Category = None
                        iris.Other_Expenses_Category = None
                        iris.Lasting_Investment_Category = None
                        iris.No_Lasting_Investment_Category = None
                        iris.depressed = None
                    iris.das1=a1
                    iris.das2=a2
                    iris.das3=a3
                    iris.das4=a4
                    iris.das5=a5
                    iris.das6=a6
                    iris.das7=a7
                    iris.das8=a8
                    iris.das_d=response_json['Depression']
                    iris.das_a=response_json['Anxiety']
                    iris.das_s=response_json['Stress']
                    iris.save()
                    return JsonResponse({'Depression':response_json['Depression'],'Panic':response_json['Anxiety'],'Bipolar':response_json['Stress']}, status=200)
                except Exception as e:
                    print(e)

                iris=Iris.objects.create(Person_email=patient,Doctor_email=last_doctor,
                                            das1=a1,das2=a2,das3=a3,das4=a4,das5=a5,das6=a6,das7=a7,das8=a8,
                                            das_d=response_json['Depression'],
                                            das_a=response_json['Anxiety'],
                                            das_s=response_json['Stress'], 
                                            Age=Age, Gender=Gender)
                return JsonResponse({'Depression':response_json['Depression'],'Panic':response_json['Anxiety'],'Bipolar':response_json['Stress']}, status=200)
        else:
            return exp_logout(request)
    return JsonResponse({'state':'error request method'}, status=201)

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
                pred=panic.predict(new_test)[0]
                pred = False if pred == 0 else True
                fields = {'Person_email': patient, 'Positive_Negative_panic': pred, "Age" : Age}
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
                "What is your general medical history?",
                "Could you provide some demographic information?",
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
            except Exception as e:
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

                
                Age = date.today().year - patient.birth.year
                Gender = "Male" if patient.gender == 'm' else "Female"
                fields = {'Person_email': patient, 'Expert_Diagnose': pred, 'Age' : Age, 'Gender' : Gender}
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
                "How often do you feel sadness?",
                "How often do you feel euphoric or extremely happy?",
                "How often do you feel exhausted?",
                "How often do you experience sleep disorders or disturbances?",
                "Do you experience frequent mood swings?",
                "Have you experienced suicidal thoughts?",
                "Have you experienced anorexia or significant loss of appetite?",
                "Do you usually respect authority figures?",
                "Do you try to explain your actions or feelings to others?",
                "Do you often respond aggressively in challenging situations?",
                "Do you tend to ignore problems and move on rather than addressing them?",
                " Have you ever had a nervous breakdown?",
                "Do you admit your mistakes when you recognize them?",
                "Do you frequently find yourself overthinking situations?",
                "How would you rate your level of sexual activity?",
                "How would you rate your concentration levels?",
                "How would you rate your level of optimism?"
            ]	
            answer=[["Usually","Sometimes","Most-Often","Seldom"],
                    ["Usually","Sometimes","Most-Often","Seldom"],
                    ["Usually","Sometimes","Most-Often","Seldom"],
                    ["Usually","Sometimes","Most-Often","Seldom"],
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
                pred = False if pred == 0 else True
                fields = {'Person_email': patient, 'depressed': pred, 'Age' :Age, 'Gender' : Gender}
                int_list = [i for i in range(0, 100)]
                answer=[["Not Married", "Married"],
                    ["0","1","2","3","4","5","6","7","8","9+"],
                    ["1","2","3","4","5","6","7","8","9","10+"],
                    ["Yes","No"],
                    ["Yes","No"],
                    ["Yes","No"],
                    ["Yes","No"],
                    ['No Education', 'Primary', 'Secondary', 'High School', 'College'],
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
                "What is your marital status?",
                "How many children do you have?",
                "How many members are there in your household?",
                "Do you receive income from a salary?",
                "Do you receive income from a business?",
                "Do you receive income from non-business sources?",
                "Is your main source of income from your primary occupation?",
                "What is your highest level of education?",
                "How would you categorize the total value of assets you have gained?",
                "How would you categorize the total value of your durable assets (e.g., house, car)?",
                "How would you categorize the total value of your savings and other liquid assets?",
                "How would you categorize your average monthly living expenses?",
                "How would you categorize your average monthly other expenses (e.g., entertainment, travel)?",
                "How would you categorize the total value of your lasting investments (e.g., real estate, bonds)?",
                "How would you categorize the total value of your non-lasting investments (e.g., stocks, cryptocurrency)?"
            ]
            answer=[["Not Married", "Married"],
                    ["0","1","2","3","4","5","6","7","8","9+"],
                    ["1","2","3","4","5","6","7","8","9","10+"],
                    ["Yes","No"],
                    ["Yes","No"],
                    ["Yes","No"],
                    ["Yes","No"],
                    ['No Education', 'Primary', 'Secondary', 'High School', 'College'],
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
                obj_res = Iris.objects.get(Person_email=p)
                
                selection=data['doctor']
                doc=Doctor.objects.get(email=selection)
                setattr(obj_res, "Doctor_email", doc)
                obj_res.save()
                return JsonResponse({'state':'success'}, status=200)
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

@csrf_exempt
def id_do_test(request): 
    if request.method == 'POST':
        data = json.loads(request.body)
        person_result=check_token(request)
        if check_token(request):
            try:
                iris=Iris.objects.get(Person_email=person_result)
                doctor=Doctor.objects.get(email=iris.Doctor_email)
                return JsonResponse({'res':True,"doctor":doctor.email,'first_name': doctor.first_name,'last_name': doctor.last_name,
                                     'specialization': doctor.specialization,'clinic_address': doctor.clinic_address,
                                     'rate': doctor.rate}, status=200)
            except:
                return JsonResponse({'res':False,"doctor":'','first_name': '','last_name': '',
                                     'specialization': '','clinic_address': '',
                                     'rate': ''}, status=200)
        else:
            return exp_logout(request)
    return JsonResponse({'state':'error request method'}, status=201)

@csrf_exempt
def patient_all_info(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        person_result=check_token(request)
        if check_token(request):
            p=data['patient']
            params=["Person_email","Gender","Age","das1","das2","das3","das4","das5","das6","das7","das8","das_d","das_a","das_s",
                    "Family_History","Personal_History","Current_Stressors","Symptoms","Severity","Impact_on_Life","Demographics",
                    "Medical_History","Psychiatric_History","Substance_Use","Coping_Mechanisms","Social_Support","Lifestyle_Factors",
                    "Positive_Negative_panic","Sadness","Euphoric","Exhausted","Sleep_Dissorder","Mood_Swing","Suicidal_Thoughts",
                    "Anorxia","Authority_Respect","Try_Explanation","Aggressive_Response","Ignore_And_Move_On","Nervous_BreakDown",
                    "Admit_Mistakes","Overthinking","Sexual_Activity","Concentration","Optimisim","Expert_Diagnose ","Married",
                    "Number_Children","total_members","incoming_salary","incoming_business","incoming_no_business","labor_primary",
                    "Education_Level","gained_asset_Category","Durable_Asset_Category","Save_Asset_Category","Living_Expenses_Category",
                    "Other_Expenses_Category","Lasting_Investment_Category","No_Lasting_Investment_Category","depressed"
                ]
            p=Patient.objects.get(email=p)
            iris=Iris.objects.get(Person_email=p)
            value=[p.email,iris.Gender,iris.Age,iris.das1,iris.das2,iris.das3,iris.das4,iris.das5,iris.das6,iris.das7,iris.das8,iris.das_d,iris.das_a,iris.das_s,
                    iris.Family_History,iris.Personal_History,iris.Current_Stressors,iris.Symptoms,iris.Severity,iris.Impact_on_Life,iris.Demographics,
                    iris.Medical_History,iris.Psychiatric_History,iris.Substance_Use,iris.Coping_Mechanisms,iris.Social_Support,iris.Lifestyle_Factors,
                    iris.Positive_Negative_panic,iris.Sadness,iris.Euphoric,iris.Exhausted,iris.Sleep_Dissorder,iris.Mood_Swing,iris.Suicidal_Thoughts,
                    iris.Anorxia,iris.Authority_Respect,iris.Try_Explanation,iris.Aggressive_Response,iris.Ignore_And_Move_On,iris.Nervous_BreakDown,
                    iris.Admit_Mistakes,iris.Overthinking,iris.Sexual_Activity,iris.Concentration,iris.Optimisim,iris.Expert_Diagnose ,iris.Married,
                    iris.Number_Children,iris.total_members,iris.incoming_salary,iris.incoming_business,iris.incoming_no_business,iris.labor_primary,
                    iris.Education_Level,iris.gained_asset_Category,iris.Durable_Asset_Category,iris.Save_Asset_Category,iris.Living_Expenses_Category,
                    iris.Other_Expenses_Category,iris.Lasting_Investment_Category,iris.No_Lasting_Investment_Category,iris.depressed
                ]
            arr={}
            j=0
            for i in params:
                arr[i]=value[j]
                j=j+1
            print(arr)
            return JsonResponse({"arr":arr})
        else:
            return exp_logout(request)
    return JsonResponse({'state':'error request method'}, status=201)