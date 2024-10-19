from rest_framework import serializers
from .models import CustomUser, PatientProfile, DoctorProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'address', 'first_name', 'last_name', 'email','nid']



class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = '__all__'

class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = '__all__'






class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)
    user_role = serializers.ChoiceField(choices=CustomUser.ROLES)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'address', 'nid', 'user_role', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        if CustomUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already exists.")
        if CustomUser.objects.filter(nid=data['nid']).exists():
            raise serializers.ValidationError("NID already exists.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            address=validated_data['address'],
            nid=validated_data['nid'],
            user_role=validated_data['user_role'],
        )
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    user_role = serializers.CharField(read_only=True)





