from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Info(models.Model):
    CHOICES = (('Member','Member'),('Convenor','Convenor'),('Admin','Admin'))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100, default="Member", choices=CHOICES)
    roll_no = models.CharField(max_length=100)

