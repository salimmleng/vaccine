
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from datetime import date
CustomUser = get_user_model()


class Vaccine(models.Model):
    image = models.URLField(max_length=200)
    name = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=100,default='default-manufacturer')
    batch_number = models.CharField(max_length=100,default='default-batch-number')
    expiry_date =  models.DateField(default=date(2024, 12, 31))
    age_limit = models.CharField(max_length=50,default=0) 
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name





