from django.db import models
from users.models import *

# Create your models here.

class Data(models.Model):
    Huggingface_API = models.CharField(max_length=100,null=True, blank=True)

    Chack_Email_URL = models.CharField(max_length=100,null=True, blank=True)
    Chack_Email_API_KEY = models.CharField(max_length=100,null=True, blank=True)
    Chack_Email_API_HOST = models.CharField(max_length=100,null=True, blank=True)
    
    Send_Mail_URL1 = models.CharField(max_length=100,null=True, blank=True)
    Send_Mail_API_KEY1 = models.CharField(max_length=100,null=True, blank=True)
    Send_Mail_API_HOST1 = models.CharField(max_length=100,null=True, blank=True)

    Send_Mail_URL2 =  models.CharField(max_length=100,null=True, blank=True)
    Send_Mail_API_KEY2 = models.CharField(max_length=100,null=True, blank=True)
    Send_Mail_API_HOST2 = models.CharField(max_length=100,null=True, blank=True)

    Whatsapp_URL =  models.CharField(max_length=100,null=True, blank=True)
    Whatsapp_Token =  models.CharField(max_length=100,null=True, blank=True)
    Whatsapp_API_KEY = models.CharField(max_length=100,null=True, blank=True)
    Whatsapp_API_HOST = models.CharField(max_length=100,null=True, blank=True)
    