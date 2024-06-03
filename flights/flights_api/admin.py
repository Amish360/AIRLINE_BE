from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Aircraft)
admin.site.register(Airline)
admin.site.register(Airport)
admin.site.register(Flight)
admin.site.register(FlightStatus)
admin.site.register(Booking)