from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView, CreateAPIView
from datetime import datetime
from django.utils import timezone

from .models import Flight, Booking
from .serializers import FlightSerializer, BookingSerializer, BookingDetailsSerializer, UpdateBookingSerializer, RegisterSerializer,BasicAccountSerializer


class FlightsList(ListAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


class BookingsList(ListAPIView):
    
    serializer_class = BookingSerializer

    def get_queryset(self):
        query = Booking.objects.filter(
            date__gte = timezone.now(),
            user = self.request.user
            )
        return query




class BookingDetails(RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingDetailsSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'booking_id'


class UpdateBooking(RetrieveUpdateAPIView):
    queryset = Booking.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'booking_id'

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return UpdateBookingSerializer
        return BasicAccountSerializer







class CancelBooking(DestroyAPIView):
    queryset = Booking.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'booking_id'


class BookFlight(CreateAPIView):
    serializer_class = UpdateBookingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, flight_id=self.kwargs['flight_id'])


class Register(CreateAPIView):
    serializer_class = RegisterSerializer
