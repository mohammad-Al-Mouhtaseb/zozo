from django.db import models
from users.models import *

# Create your models here.
class To_Do(models.Model):
    doctor = models.ForeignKey(Doctor, null=True,related_name='doctor_appointments', on_delete=models.DO_NOTHING)
    patient = models.ForeignKey(Patient, null=True,related_name='patient_appointments', on_delete=models.CASCADE)
    aim=models.CharField(max_length=100)
    goal=models.CharField(max_length=100)
    is_done=models.BooleanField(default=False)

    def __str__(self):
        return f'from: {self.doctor}     |||     to: {self.patient}     |||     Aim: {self.aim}     |||     Goal: {self.goal}'
    
    class Meta:
        verbose_name = 'To_Do_list'
        ordering = ['patient_id']