from django.test import TestCase
from accounts.forms import SignUpForm, ProfileForm

class TestSignUpForm(TestCase):
	def test_valid_data(self):
		form = SignUpForm(data={'mobile_phone':'09024985124'})
		self.assertTrue(form.is_valid())

	def test_invalid_data(self):
		form = SignUpForm(data={})
		self.assertFalse(form.is_valid())
		self.assertEqual(len(form.errors), 1)


class TestProfileForm(TestCase):
	def test_valid_data(self):
		form = ProfileForm(data={'first_name':'behrad', 'last_name':'peikani', 'gender':'Male',
		 'email': 'behradpeikani@gmail.com'})
		self.assertTrue(form.is_valid())

	def test_invalid_data(self):
		form = ProfileForm(data={'first_name':'behrad', 'last_name':'peikani', 'gender':'Male',
		 'email': 'ndlkvmfhsuifhius'})
		self.assertFalse(form.is_valid())
		self.assertEqual(len(form.errors), 1)