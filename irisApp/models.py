from django.db import models
from users.models import *
from datetime import date

# Create your models here.

class Iris(models.Model):
    Person_email = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True, related_name='Person_Id')
    Doctor_email = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True, related_name='Doctor_Id') 

    das1=models.IntegerField(null=True, blank=True)#EXP
    das2=models.IntegerField(null=True, blank=True)#EXP
    das3=models.IntegerField(null=True, blank=True)#EXP
    das4=models.IntegerField(null=True, blank=True)#EXP
    das5=models.IntegerField(null=True, blank=True)#EXP
    das6=models.IntegerField(null=True, blank=True)#EXP
    das7=models.IntegerField(null=True, blank=True)#EXP
    das8=models.IntegerField(null=True, blank=True)#EXP
    das_d=models.BooleanField(default=False, null=True, blank=True)#EXP_res
    das_a=models.BooleanField(default=False, null=True, blank=True)#EXP_res
    das_s=models.BooleanField(default=False, null=True, blank=True)#EXP_res

    Age=models.IntegerField(null=True, blank=True)#Panic_Disorder
    Gender=models.IntegerField(null=True, blank=True)#Panic_Disorder
    Family_History=models.IntegerField(null=True, blank=True)#Panic_Disorder
    Personal_History=models.IntegerField(null=True, blank=True)#Panic_Disorder
    Current_Stressors=models.IntegerField(null=True, blank=True)#Panic_Disorder
    Symptoms=models.IntegerField(null=True, blank=True)#Panic_Disorder
    Severity=models.IntegerField(null=True, blank=True)#Panic_Disorder
    Impact_on_Life=models.IntegerField(null=True, blank=True)#Panic_Disorder
    Demographics=models.IntegerField(null=True, blank=True)#Panic_Disorder
    Medical_History=models.IntegerField(null=True, blank=True)#Panic_Disorder
    Psychiatric_History=models.IntegerField(null=True, blank=True)#Panic_Disorder
    Substance_Use=models.IntegerField(null=True, blank=True)#Panic_Disorder
    Coping_Mechanisms=models.IntegerField(null=True, blank=True)#Panic_Disorder
    Social_Support=models.IntegerField(null=True, blank=True)#Panic_Disorder
    Lifestyle_Factors=models.IntegerField(null=True, blank=True)#Panic_Disorder
    Positive_Negative=models.BooleanField(null=True, blank=True)#Panic_Disorder_res

    Sadness = models.IntegerField(null=True, blank=True)#Dep_Bi
    Euphoric = models.IntegerField(null=True, blank=True)#Dep_Bi
    Exhausted = models.IntegerField(null=True, blank=True)#Dep_Bi
    Sleep_Dissorder = models.IntegerField(null=True, blank=True)#Dep_Bi
    Mood_Swing = models.IntegerField(null=True, blank=True)#Dep_Bi
    Suicidal_Thoughts = models.IntegerField(null=True, blank=True)#Dep_Bi
    Anorxia = models.IntegerField(null=True, blank=True)#Dep_Bi
    Authority_Respect = models.IntegerField(null=True, blank=True)#Dep_Bi
    Try_Explanation = models.IntegerField(null=True, blank=True)#Dep_Bi
    Aggressiv_Response = models.IntegerField(null=True, blank=True)#Dep_Bi
    Ignore_And_Move_On = models.IntegerField(null=True, blank=True)#Dep_Bi
    Nervous_BreakDown = models.IntegerField(null=True, blank=True)#Dep_Bi
    Admin_Mistakes = models.IntegerField(null=True, blank=True)#Dep_Bi
    Overthinking = models.IntegerField(null=True, blank=True)#Dep_Bi
    Sexual_Activity = models.IntegerField(null=True, blank=True)#Dep_Bi
    Concentration = models.IntegerField(null=True, blank=True)#Dep_Bi
    Optimisim = models.IntegerField(null=True, blank=True)#Dep_Bi
    Expert_Diagnose = models.IntegerField(null=True, blank=True)#Dep_Bi_res

    # Age...Panic_Disorder
    # Gender...Panic_Disorder 
    # Married=   
    # Number_Children=
    # Education_Level=


    def __str__(self):
        return  str(self.Person_email)
    
    class Meta:
        verbose_name = 'IRIS'