from rest_framework import viewsets
from .models import Listing, Booking
from .serializer import ListingSerializer, BookingSerializer

class ListingViewSet(viewsets.ModelViewSet):
    """
    Provides a CRUD endpoint for Listing models:
    list, retrieve, create, update, and partial_update, distory.
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    """
    Provides a CRUD endpoints for Booking models:
    list, retrieve, create, update, and partial_update, distory.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_queryset(self):
        """
        provides CRUD endpoints for Booking model.
        """
        queryset = Booking.objects.all()
        serializer_class = BookingSerializer

import requests
import uuid
from django.conf import settings
from django.http import JsonResponse
from .models import Payment

CHAPA_API_URL = "https://api.chapa.co/v1/transaction/initialize"

def initiate_payment(request):
    # Assume booking data comes from request.POST (adjust as needed)
    amount = request.POST.get("amount")
    booking_reference = request.POST.get("booking_reference")
    email = request.POST.get("email")
    first_name = request.POST.get("first_name", "Guest")
    last_name = request.POST.get("last_name", "")

    tx_ref = str(uuid.uuid4())  # Unique transaction ref

    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "amount": amount,
        "currency": "ETB",
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "tx_ref": tx_ref,
        "callback_url": "http://yourdomain.com/api/payment/verify/",  # adjust
        "return_url": "http://yourdomain.com/payment/complete/",      # adjust
        "customization": {
            "title": "Booking Payment",
            "description": f"Payment for booking {booking_reference}"
        }
    }

    response = requests.post(CHAPA_API_URL, json=data, headers=headers)

    if response.status_code == 200 and response.json()["status"] == "success":
        # Save transaction
        Payment.objects.create(
            booking_reference=booking_reference,
            amount=amount,
            chapa_tx_ref=tx_ref,
            chapa_status="Pending"
        )
        return JsonResponse({"payment_url": response.json()["data"]["checkout_url"]})
    else:
        return JsonResponse({"error": "Payment initiation failed"}, status=400)
