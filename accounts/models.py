from django.db import models
from django.contrib.auth.models import User
from base.models import Club

# Create your models here.
class Info(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=100)
    
class Permission(models.Model):
    actions = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.actions[:20]

class Role(models.Model):

    MEMBER = 'member'
    CONVENOR = 'convenor'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (MEMBER, 'Member'),
        (CONVENOR, 'Convenor'),
        (ADMIN, 'Admin')
    ]

    name = models.CharField(max_length=50, choices=ROLE_CHOICES, default=MEMBER)
    permissions = models.ManyToManyField(Permission, blank=True, null=True)

    def __str__(self):
        return self.name

class Permission_Assignment(models.Model):
    club = models.ForeignKey(Club,blank=True, null = True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=False, null = False, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, blank=False, null = False, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.club_id) + " " + str(self.user_id) + " " + str(self.role.name)
