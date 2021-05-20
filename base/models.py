from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Club(models.Model):
    #Many Clubs have many Users
    users = models.ManyToManyField(User, blank=True, null=True)
    club_name =  models.CharField(max_length = 100)
    logo = models.ImageField(upload_to="images/", default = "")

    def __str__(self):
        return self.club_name

class Item(models.Model):
    item_name = models.CharField(max_length=100)
    qty = models.IntegerField()
    club = models.ForeignKey(Club, blank=True, null = True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/", default = "")  

    def __str__(self):
        return self.item_name

class Request(models.Model):
    STATUS = (('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected'))
    requested_by = models.ForeignKey(User, null=True, on_delete = models.SET_NULL)
    item = models.ForeignKey(Item, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=100, null=True, choices=STATUS)
    date_created = models.DateField(auto_now_add=True)
    

