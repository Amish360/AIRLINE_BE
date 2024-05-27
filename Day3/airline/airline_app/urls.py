from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FlightViewSet,AirlineViewSet,AirportViewSet,AircraftViewSet,FlightSearchAPIView,AirlineSearchAPIView,book_flight,cancel_booking

router = DefaultRouter()
router.register(r'flights', FlightViewSet)
router.register(r'airlines', AirlineViewSet)
router.register(r'airport', AirportViewSet)
router.register(r'aircraft', AircraftViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('search/flights/', FlightSearchAPIView.as_view(), name='flight-search'),
    path('search/airlines/', AirlineSearchAPIView.as_view(), name='airline-search'),
     path('book-flight/', book_flight, name='book-flight'),
      path('cancel-booking/<int:booking_id>/', cancel_booking, name='cancel-booking'),
]
