from django.shortcuts import render
from rest_framework import viewsets
from .models import Flight
from .serializers import FlightSerializer
# Create your views here.

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer