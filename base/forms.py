from django import forms
from django.forms import ModelForm

from base.models import Club, Item

class ClubForm(forms.ModelForm):
    
    class Meta:
        model = Club
        fields = '__all__'

class ItemForm(forms.ModelForm):
    
    class Meta:
        model = Item
        fields = '__all__'
