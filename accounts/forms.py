from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from accounts.models import Info, Permission_Assignment

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class InfoForm(forms.ModelForm):
    class Meta:
        model = Info
        fields = ['roll_no', 'user']

class PermissionAssignmentForm(forms.ModelForm):
    class Meta:
        model = Permission_Assignment
        fields = ['club','user', 'role']