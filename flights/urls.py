from django.urls import path
from . import views

app_name = 'flights'
urlpatterns = [
	path('', views.SearchFlight.as_view(), name='search_flight'),
	path('booking_flight/', views.BookingFlightView.as_view(), name='booking_flight'),
	path('see_booking/<int:pk>/', views.SeeBookingView.as_view(), name='see_booking'),
]