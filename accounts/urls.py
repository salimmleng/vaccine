# modified

from django.urls import path
from .views import UserRegistrationAPIView, UserProfileView, ChangePasswordAPIView,UserLoginApiView,UserLogoutApiView,activate

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('login/', UserLoginApiView.as_view(), name='login'),
    path('logout/', UserLogoutApiView.as_view(), name='logout'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='user-profile'),
    path('active/<uid64>/<token>', activate, name='activate'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='change_password'),
]

