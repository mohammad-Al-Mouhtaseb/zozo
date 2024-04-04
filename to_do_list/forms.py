from django import forms
from . models import *
class add_goal(forms.ModelForm):
    class Meta:
        model = To_Do
        fields = '__all__'