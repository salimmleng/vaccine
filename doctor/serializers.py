
from rest_framework import serializers
from .models import Vaccine,Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class VaccineSerializer(serializers.ModelSerializer):

    # category = serializers.SlugRelatedField(
    #     queryset=Category.objects.all(),
    #     slug_field='name' 
    # ) 

    class Meta:
        model = Vaccine
        fields = ['id', 'image', 'name', 'manufacturer','batch_number','expiry_date', 'age_limit', 'description','created_at', 'created_by']
        read_only_fields = ['created_by',]

