from django.db import models
from users.models import *
from datetime import date

# Create your models here.

class Panic_Disorder(models.Model):
    Person_email = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True, related_name='Person_Id')
    Doctor_email = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True, related_name='Doctor_Id') 
    Positive_Negative=models.BooleanField(null=True, blank=True)
    Family_History=models.IntegerField(null=True, blank=True)
    Personal_History=models.IntegerField(null=True, blank=True)
    Current_Stressors=models.IntegerField(null=True, blank=True)
    Symptoms=models.IntegerField(null=True, blank=True)
    Severity=models.IntegerField(null=True, blank=True)
    Impact_on_Life=models.IntegerField(null=True, blank=True)
    Demographics=models.IntegerField(null=True, blank=True)
    Medical_History=models.IntegerField(null=True, blank=True)
    Psychiatric_History=models.IntegerField(null=True, blank=True)
    Substance_Use=models.IntegerField(null=True, blank=True)
    Coping_Mechanisms=models.IntegerField(null=True, blank=True)
    Social_Support=models.IntegerField(null=True, blank=True)
    Lifestyle_Factors=models.IntegerField(null=True, blank=True)


    def __str__(self):
        return  str(self.Person_email)
    
    class Meta:
        verbose_name = 'Panic_Disorder'
        # ordering = ['Person_email']