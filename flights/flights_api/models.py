from django.db import models
from django.conf import settings
class Airport(models.Model):
    code = models.CharField(max_length=10)  # IATA or ICAO code
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Airline(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10)  # IATA or ICAO code

    def __str__(self):
        return self.name

class Aircraft(models.Model):
    model = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.manufacturer} {self.model}"

class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    origin = models.ForeignKey(Airport, related_name='departures', on_delete=models.CASCADE)
    destination = models.ForeignKey(Airport, related_name='arrivals', on_delete=models.CASCADE)
    scheduled_departure = models.DateTimeField()
    scheduled_arrival = models.DateTimeField()
    status = models.CharField(max_length=50, choices=[
        ('Scheduled', 'Scheduled'),
        ('On Time', 'On Time'),
        ('Delayed', 'Delayed'),
        ('Cancelled', 'Cancelled'),
        ('Landed', 'Landed')
    ])
    
    def __str__(self):
        return f"{self.airline.code} {self.flight_number} from {self.origin.code} to {self.destination.code}"


class FlightStatus(models.Model):
    flight = models.OneToOneField(Flight, on_delete=models.CASCADE)
    updated_departure = models.DateTimeField(null=True, blank=True)
    updated_arrival = models.DateTimeField(null=True, blank=True)
    gate = models.CharField(max_length=10, null=True, blank=True)
    remarks = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Status of {self.flight}"


