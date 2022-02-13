from django.test import TestCase, Client
from django.urls import reverse
from accounts.forms import SignUpForm
from accounts.models import User, Profile


class TestView(TestCase):
	def setUp(self):
		self.client = Client()

	def test_user_sign_up_GET(self):
		response = self.client.get(reverse('accounts:sign_up'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'accounts/sign_up.html')
		self.assertEqual(response.context['form'], SignUpForm)

	def test_user_sign_up_POST_valid(self):
		response = self.client.post(reverse('accounts:sign_up'), data={
			'mobile_phone':'09024985124',
		})
		self.assertEqual(response.status_code, 302)

	def test_user_sign_up_POST_invalid(self):
		response = self.client.post(reverse('accounts:sign_up'), data={
			'mobile_phone':'',
		})
		self.assertEqual(response.status_code, 200)
		self.assertFalse(response.context['form'].is_valid())
		self.assertFormError(response, 'form', field='mobile_phone', errors=['This field is required.'])