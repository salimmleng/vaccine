from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model, authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from rest_framework import status

from . import serializers
from . import models

User = get_user_model()

class UserRegistrationAPIView(APIView):
    serializer_class = serializers.RegistrationSerializer
    permission_classes = [AllowAny] 

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"https://vaccination-management-wbw3.onrender.com/accounts/active/{uid}/{token}"
            email_subject = "Confirm your email"
            email_body = render_to_string('confirm_email.html', {'confirm_link': confirm_link})
            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response("Check your mail for confirmation", status=201)
        return Response(serializer.errors, status=400)

def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("https://salimmleng.github.io/vaccine-management/login.html")
    else:
        return redirect("register")




class UserLoginApiView(APIView):
    permission_classes = [AllowAny] 
    def post(self, request):
        serializer = serializers.UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)
                return Response({"token": token.key, 'user_id': user.id,'user_role': user.user_role}, status=200)
            else:
                return Response({"error": "Invalid credentials"}, status=400)
        return Response(serializer.errors, status=400)

class UserLogoutApiView(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return redirect('login')


class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.user_role == 'patient':
            profile = models.PatientProfile.objects.get(user=user)
            serializer = serializers.PatientProfileSerializer(profile)
        elif user.user_role == 'doctor':
            profile = models.DoctorProfile.objects.get(user=user)
            serializer = serializers.DoctorProfileSerializer(profile)
        else:
            return Response({'error': 'Invalid role'}, status=400)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        if user.user_role == 'patient':
            profile = models.PatientProfile.objects.get(user=user)
            serializer = serializers.PatientProfileSerializer(profile, data=request.data)
        elif user.user_role == 'doctor':
            profile = models.DoctorProfile.objects.get(user=user)
            serializer = serializers.DoctorProfileSerializer(profile, data=request.data)
        else:
            return Response({'error': 'Invalid role'}, status=400)
           
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)



class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not user.check_password(old_password):
            return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

        if not new_password:
            return Response({'error': 'New password is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password changed successfully'}, status=200)




class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        user = get_object_or_404(models.CustomUser, pk=pk)
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)
    

    def put(self, request, pk, format=None):
        user = get_object_or_404(models.CustomUser, pk=pk)
        serializer = serializers.UserSerializer(user, data=request.data, partial=True)  # partial=True allows for partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

