from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Club(models.Model):
    #Many Clubs have one User
    users = models.ManyToManyField(User, blank=True, null=True)
    club_name =  models.CharField(max_length = 100)
    logo = models.ImageField(upload_to="images/", default = "")

    def __str__(self):
        return self.club_name
