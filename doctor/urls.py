# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .import views
# router = DefaultRouter()

# router.register('vaccine', views.VaccineViewSet)
# router.register('doctor_list', views.DoctorViewSet)
# urlpatterns = [
#     path('', include(router.urls)),
# ]


# mod 

from django.urls import path, include
from .views import VaccineViewSet,VaccineDetailViewSet

urlpatterns = [
   
    path('api/vaccines/',VaccineViewSet.as_view(), name='add_vaccine'),
    path('api/vaccines/<int:pk>/',VaccineDetailViewSet.as_view(), name='add_vaccine'),
]



