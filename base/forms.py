from django import forms
from django.forms import ModelForm

from base.models import Club

class ClubForm(forms.ModelForm):
    
    class Meta:
        model = Club
        fields = '__all__'
