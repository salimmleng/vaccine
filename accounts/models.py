from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    ROLES=[
        ('patient','Patient'),
        ('doctor','Doctor'),
    ]

    user_role = models.CharField(max_length=50,choices=ROLES,null=True,blank=True)
    nid = models.CharField(max_length=30,unique=True,blank=True,null=True)
    address = models.CharField(max_length=100,blank=True,null=True)
   

    def __str__(self):
        return self.username





class PatientProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
   
class DoctorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)


