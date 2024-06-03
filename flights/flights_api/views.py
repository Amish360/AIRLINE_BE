from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets,generics
from .models import Flight,Aircraft,Airline,Airport,Booking
from .serializers import FlightSerializer,AircraftSerializer,AirlineSerializer,AirportSerializer,BookingSerializer

CustomUser = get_user_model()


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

@api_view(["GET"])
def flight_search(request):
    flight_number = request.GET.get("flightnumber", "")

    # Query to filter based on the flight_number field in the Flight model
    if flight_number:
        flights = Flight.objects.filter(flight_number__icontains=flight_number).order_by('flight_number')
    else:
        flights = Flight.objects.all().order_by('flight_number')

    # Serialize the flights using the serializer
    serializer = FlightSerializer(flights, many=True)

    return Response({"results": serializer.data})
    
   
@api_view(['POST'])
def book_flight(request):
    # Get the authenticated user using CustomUser model
    user_id = request.data.get('user_id')  # Assuming user_id is provided in request data
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

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