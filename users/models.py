from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Abo(User):
    country=models.CharField(max_length=50,default='sy',null=True, blank=True)
    gender=models.CharField(max_length=10,choices=[("m", "m"),("f", "f")],default='m',null=True, blank=True)
    birth=models.DateField(default='2000-1-1',null=True, blank=True)
    photo=models.ImageField(upload_to='users/photos', default='users/photos/default.png',null=True)
    language=models.CharField(max_length=10,choices=[("en", "en"),("ar", "ar")], default='en',null=True, blank=True)
    token=models.CharField(max_length=50,default='',null=True, blank=True)
    type=models.CharField(max_length=10,choices=[("doctor", "doctor"),("patient", "patient")], default='patient',null=True, blank=True)
    class Meta:
        abstract = True
class Patient(Abo):
    
    def __str__(self):
        return str(self.username)
    
    class Meta:
        verbose_name = 'Patient'
        ordering = ['id']

class Doctor(Abo):
    clinic_address=models.CharField(max_length=50,null=True, blank=True)
    rate=models.DecimalField(max_digits=2, decimal_places=1, default=0.0, null=True, blank=True)
    num_of_rate=models.DecimalField(max_digits=5, decimal_places=1, default=0.0, null=True, blank=True)
 

    def __str__(self):
        return str(self.username)
    
    class Meta:
        verbose_name = 'Doctor'
        ordering = ['id']