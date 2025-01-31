from rest_framework import viewsets
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer
from .tasks import send_booking_confirmation_email


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
    def perform_create(self, serializer):
        booking = serializer.save()
        user_email = booking.user.email
        booking_details = f"Destination: {booking.destination}, Date: {booking.date}"
        
        # Trigger Celery task asynchronously
        send_booking_confirmation_email.delay(user_email, booking_details)

