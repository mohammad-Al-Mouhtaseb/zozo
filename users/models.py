from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Patient(User):
    
    def __str__(self):
        return str(self.username)
    
    class Meta:
        verbose_name = 'Patient'
        ordering = ['id']

class Doctor(User):
    clinic_address=models.CharField(max_length=50,null=True, blank=True)
    rate=models.DecimalField(max_digits=2, decimal_places=1, default=0.0, null=True, blank=True)
    num_of_rate=models.DecimalField(max_digits=5, decimal_places=1, default=0.0, null=True, blank=True)
 

    def __str__(self):
        return str(self.username)
    
    class Meta:
        verbose_name = 'Doctor'
        ordering = ['id']