from django.db import models

# Create your models here.
class Club(models.Model):
    club_name =  models.CharField(max_length = 100)
    logo = models.ImageField(upload_to="images/", default = "")

    def __str__(self):
        return self.club_name