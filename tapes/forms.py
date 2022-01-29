from django import forms
from tapes.models import comment,post
from django.contrib.auth.models import User

class Form(forms.ModelForm):
    class Meta:
        model = comment
        fields= ['text']

class Form_post(forms.ModelForm):
    class Meta:
        model = post
        fields= ["user",'title','text','image','type_ch']


