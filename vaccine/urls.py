
from django.urls import path
from .views import DoseListCreateView, DoseDetailView, AvailableHospitalListView, AvailableDatesListView,ReviewView

urlpatterns = [
    path('api/doses/', DoseListCreateView.as_view(), name='dose-list-create'),
    path('api/doses/<int:pk>/', DoseDetailView.as_view(), name='dose-detail'),
    path('api/available_hospitals/', AvailableHospitalListView.as_view(), name='available-hospitals-list'),
    path('api/available_dates/', AvailableDatesListView.as_view(), name='available-dates-list'),
    path('reviews/', ReviewView.as_view(), name='review-create'),
    path('reviews/<int:vaccine_id>/', ReviewView.as_view(), name='review-create'),
]

