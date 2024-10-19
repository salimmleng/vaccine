from django.db import models
from django.conf import settings
from doctor.models import Vaccine


VACCINE_STATUS = [
    ('Completed','Completed'),
    ('Pending','Pending'),
]

class AvailableHospital(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class AvailableDates(models.Model):
    date = models.DateField()
    
    def __str__(self):
        return self.date.strftime('%Y-%m-%d')


class Dose(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    vaccine_status = models.CharField(choices=VACCINE_STATUS,max_length=20,default='Pending')
    vaccine_center = models.ForeignKey(AvailableHospital, on_delete=models.CASCADE)
    firstDose_date = models.ForeignKey(AvailableDates, on_delete=models.CASCADE,related_name='first_doses',null=True,blank=True)

    secondDose_date = models.ForeignKey(AvailableDates, on_delete=models.CASCADE,related_name='second_doses',null=True,blank=True)

    mobile_no = models.CharField(max_length=12,default=00)
   
    def __str__(self):
        return f"{self.user} - {self.vaccine.name}"
    


STAR_CHOICES =[
    ('⭐','⭐'),
    ('⭐⭐','⭐⭐'),
    ('⭐⭐⭐','⭐⭐⭐'),
    ('⭐⭐⭐⭐','⭐⭐⭐⭐'),
    ('⭐⭐⭐⭐⭐','⭐⭐⭐⭐⭐'),
]



class Review(models.Model):

    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.CharField(max_length=50,choices=STAR_CHOICES)


    def __str__(self):
        return f"Patient: {self.reviewer.first_name} on Vaccine: {self.vaccine.name} "



