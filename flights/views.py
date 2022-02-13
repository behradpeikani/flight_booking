from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from .models import Flight, Book
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from decimal import Decimal


class SearchFlight(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'flights/search_flight.html')

	def post(self, request, *args, **kwargs):
		source = request.POST.get('source')
		destination = request.POST.get('destination')
		date = request.POST.get('date')
		flight_list = Flight.objects.filter(source=source, destination=destination, date=date)
		if flight_list:
			return render(request, 'flights/flight_list.html', locals())
		else:
			messages.error(request, 'No flights available', 'warning')
			return render(request, 'flights/search_flight.html')


class BookingFlightView(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		return render(request, 'flights/booking_flight.html')

	def post(self, request, *args, **kwargs):
		flight_id = request.POST.get('flight_id')
		seats = request.POST.get('number_of_seats')
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		gender = request.POST.get('gender')
		email = request.POST.get('email')
		flight = Flight.objects.get(id=flight_id)
		if flight:
			if flight.number_of_seats_remaining > Decimal(seats):
				flight_name = flight.flight_name
				cost = Decimal(seats) * flight.price
				source = flight.source
				destination = flight.destination
				number_of_seats = Decimal(flight.number_of_seats)
				price = flight.price
				date = flight.date
				time = flight.time
				number_of_seats_remaining = flight.number_of_seats_remaining - Decimal(seats)
				Flight.objects.filter(id=flight_id).update(number_of_seats_remaining=number_of_seats_remaining)
				book = Book.objects.create(flight_name=flight_name, user=request.user, first_name=first_name, last_name=last_name,
										gender=gender, email=email,
										source=source, flight_id=flight_id,
										destination=destination, price=price, 
										number_of_seats=seats, date=date, time=time)
				book.save()
				return render(request, 'flights/booking_flight.html', locals())
				return redirect('flights:search_flight')
			else:
				messages.error(request, 'Sorry, select fewer number of seats', 'warning')
				return render(request, 'flights/search_flight.html')


class SeeBookingView(LoginRequiredMixin, ListView):
	template_name = 'flights/see_booking.html'
	model = Book
	context_object_name = 'book_list'

	def get_queryset(self):
		return self.model.objects.filter(user=self.request.user)