from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets,generics
from .models import Flight,Aircraft,Airline,Airport,Booking
from .serializers import FlightSerializer,AircraftSerializer,AirlineSerializer,AirportSerializer,BookingSerializer

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    
class AircraftViewSet(viewsets.ModelViewSet):
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer

class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer

class AirlineViewSet(viewsets.ModelViewSet):
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer

class FlightSearchAPIView(generics.ListAPIView):
    serializer_class = FlightSerializer

    def get_queryset(self):
        queryset = Flight.objects.all()
        query = self.request.query_params.get('q')
        if query:
            queryset = queryset.filter(
                Q(flight_number__icontains=query) |
                Q(airline__name__icontains=query) |
                Q(aircraft__model__icontains=query) |
                Q(origin__name__icontains=query) |
                Q(destination__name__icontains=query) |
                Q(scheduled_departure__icontains=query) |
                Q(scheduled_arrival__icontains=query) |
                Q(status__icontains=query)
            )
        return queryset

class AirlineSearchAPIView(generics.ListAPIView):
    serializer_class = AirlineSerializer

    def get_queryset(self):
        queryset = Airline.objects.all()
        query = self.request.query_params.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(code__icontains=query)
            )
        return queryset
    
    
@api_view(['POST'])
def book_flight(request):
    user = request.user
    flight_id = request.data.get('flight_id')

    # Ensure flight exists
    try:
        flight = Flight.objects.get(id=flight_id)
    except Flight.DoesNotExist:
        return Response({'error': 'Flight not found'}, status=status.HTTP_404_NOT_FOUND)

    # Create a new booking
    booking = Booking.objects.create(user=user, flight=flight)
    serializer = BookingSerializer(booking)

    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
def cancel_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
    except Booking.DoesNotExist:
        return Response({'error': 'Booking not found or not authorized to delete this booking.'}, status=status.HTTP_404_NOT_FOUND)

    booking.delete()
    return Response({'message': 'Booking cancelled successfully'}, status=status.HTTP_204_NO_CONTENT)