from django.test import SimpleTestCase
from django.urls import reverse, resolve
from flights.views import SearchFlight, BookingFlightView, SeeBookingView


class TestUrls(SimpleTestCase):
	def test_search_flight(self):
		url = reverse('flights:search_flight') 
		self.assertEqual(resolve(url).func.view_class, SearchFlight)

	def test_booking_flight(self):
		url = reverse('flights:booking_flight')
		self.assertEqual(resolve(url).func.view_class, BookingFlightView)

	def test_see_booking(self):
		url = reverse('flights:see_booking', args=[1,])
		self.assertEqual(resolve(url).func.view_class, SeeBookingView)