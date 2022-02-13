from django.db import models
from accounts.models import User


class Flight(models.Model):
	flight_name = models.CharField(max_length=30)
	source = models.CharField(max_length=30)
	destination = models.CharField(max_length=30)
	number_of_seats = models.DecimalField(decimal_places=0, max_digits=2)
	number_of_seats_remaining = models.DecimalField(decimal_places=0, max_digits=2)
	price = models.DecimalField(decimal_places=0, max_digits=15)
	date = models.DateField()
	time = models.TimeField()

	def __str__(self):
		return self.flight_name


class Book(models.Model):
	GENDER = (
		('Male', 'Male'),
		('Female', 'Female')
		)

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	gender = models.CharField(max_length=10, choices=GENDER)
	email = models.EmailField()
	flight_id=models.DecimalField(decimal_places=0, max_digits=2)
	flight_name = models.CharField(max_length=30)
	source = models.CharField(max_length=30)
	destination = models.CharField(max_length=30)
	number_of_seats = models.DecimalField(decimal_places=0, max_digits=2)
	price = models.DecimalField(decimal_places=0, max_digits=6)
	date = models.DateField()
	time = models.TimeField()

	def __str__(self):
		return f'{self.flight_name}-{self.flight_id}'