from rest_framework import viewsets
from .models import AvailableHospital, AvailableDates, Dose,Review
from .serializers import AvailableHospitalSerializer, AvailableDatesSerializer, DoseSerializer,ReviewSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from datetime import timedelta,datetime
from django.shortcuts import render


class DoseListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.user_role == 'doctor':
            doses = Dose.objects.all()
        else:
            doses = Dose.objects.filter(user=request.user)
        
        serializer = DoseSerializer(doses, many=True)
        return Response(serializer.data)


    def post(self, request):
        data = request.data.copy()

        first_dose_date_id = data.get('firstDose_date_id')
        if first_dose_date_id:
            try:
                first_dose_date_obj = AvailableDates.objects.get(id=first_dose_date_id)
                
                # second dose date
                second_dose_date_value = first_dose_date_obj.date + timedelta(days=21)
                
                # Get or create the second dose date object
                second_dose_date_obj, created = AvailableDates.objects.get_or_create(date=second_dose_date_value)
                
                
                data['firstDose_date_id'] = first_dose_date_obj.id
                data['secondDose_date_id'] = second_dose_date_obj.id
            except AvailableDates.DoesNotExist:
                return Response({"error": "Invalid date ID for firstDose_date."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "firstDose_date_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = DoseSerializer(data=data)
        if serializer.is_valid():
            try:
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      



    def patch(self, request):
        if request.user.user_role != 'doctor':
            return Response({"error": "Only doctors can perform bulk updates."}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        for item in data:
            try:
                dose = Dose.objects.get(pk=item['id'])
                serializer = DoseSerializer(dose, data=item, partial=True)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Dose.DoesNotExist:
                return Response({"error": f"Dose with id {item['id']} not found."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"message": "Doses updated successfully"}, status=status.HTTP_200_OK)




class DoseDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            if user.user_role == 'doctor':
                return Dose.objects.get(pk=pk)
            else:
                return Dose.objects.get(pk=pk, user=user)
        except Dose.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        dose = self.get_object(pk, request.user)
        serializer = DoseSerializer(dose)
        return Response(serializer.data)

    def put(self, request, pk):
        dose = self.get_object(pk, request.user)
        serializer = DoseSerializer(dose, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        dose = self.get_object(pk, request.user)
        serializer = DoseSerializer(dose, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
    def delete(self, request, pk):
        dose = self.get_object(pk, request.user)
        dose.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    



class ReviewView(APIView):
   
    def post(self, request, format=None):
        # Only authenticated users can post reviews
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication is required to post a review.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(reviewer=request.user)  # Save the review with the authenticated user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, vaccine_id=None, format=None):
        if vaccine_id is not None:
            reviews = Review.objects.filter(vaccine_id=vaccine_id)
        else:
            reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)








class AvailableHospitalListView(APIView):
    def get(self, request):
        hospitals = AvailableHospital.objects.all()
        serializer = AvailableHospitalSerializer(hospitals, many=True)
        return Response(serializer.data)

class AvailableDatesListView(APIView):
    def get(self, request):
        dates = AvailableDates.objects.all()
        serializer = AvailableDatesSerializer(dates, many=True)
        return Response(serializer.data)
    



# for payment gatway


from sslcommerz_lib import SSLCOMMERZ
from django.http import JsonResponse
import random
import string
import json
from django.views.decorators.csrf import csrf_exempt

def unique_transaction_id__generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@csrf_exempt
def payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Extract order and payment information from request
        total_amount = data.get('total_price')
        full_name = data.get('full_name')
        email = data.get('email')
        address = data.get('address')
        city = data.get('city')
        cus_phone = "01500000000"  

        settings = {
            'store_id': 'vacci671f23287e323',
            'store_pass': 'vacci671f23287e323@ssl',
            'issandbox': True
        }

        sslcz = SSLCOMMERZ(settings)
        
        # Define the post body for SSLCOMMERZ session
        post_body = {
            'total_amount': total_amount,
            'currency': "BDT",
            'tran_id': unique_transaction_id__generator(),
            'success_url': "https://vaccine-pi.vercel.app/vaccine/success/",
            'fail_url': "https://vaccine-pi.vercel.app/vaccine/fail/",
            'cancel_url': "https://vaccine-pi.vercel.app/vaccine/cancel/",
            'emi_option': 0,
            'cus_name': full_name,
            'cus_email': email,
            'cus_phone': cus_phone,
            'cus_add1': address,
            'cus_city': city,
            'cus_country': "Bangladesh",
            'shipping_method': "NO",
            'product_name': "Vaccine",
            'product_category': "vaccine",
            'product_profile': "general"
        }

        # Create SSLCOMMERZ session
        response = sslcz.createSession(post_body)
        print(response)
        if 'GatewayPageURL' in response:
            return JsonResponse({'GatewayPageURL': response['GatewayPageURL']})
        else:
            return JsonResponse({'error': 'Failed to create payment session'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    

@csrf_exempt
def PaymentSuccessView(request):
    return render(request, "success.html")

@csrf_exempt
def PaymentFailView(request):
    return render(request, "fail.html")

@csrf_exempt
def PaymentCancelView(request):
    return render(request, "cancel.html")