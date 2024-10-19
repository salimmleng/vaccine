
from rest_framework import serializers
from .models import Vaccine

class VaccineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccine
        fields = ['id', 'image', 'name', 'manufacturer','batch_number','expiry_date', 'age_limit', 'created_at', 'created_by']
        read_only_fields = ['created_by',]

