from django.db import models
from users.models import *
from datetime import date

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'from: {self.sender.email} to: {self.receiver.email} at {self.timestamp.strftime("%Y-%m-%d %H:%M:%S")}'
