from django.db import models
from django.utils import timezone

# Create your models here.

class Music(models.Model):
    doctor = models.EmailField(blank=True, default='')
    patient = models.EmailField(blank=True, default='')
    music = models.FileField(upload_to='sounds/music', null=True, blank=True)
    music_path = models.CharField(max_length=50,null=True, blank=True)
    type = models.CharField(max_length=50,default='',null=True, blank=True)

    def __str__(self):
        return str(self.music_path).split("/")[-1]
