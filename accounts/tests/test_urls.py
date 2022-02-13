from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import SignUpView, SignOutView, PhoneVerificationView, DashboardView


class TestUrls(SimpleTestCase):
	def test_sign_up(self):
		url = reverse('accounts:sign_up') 
		self.assertEqual(resolve(url).func.view_class, SignUpView)

	def test_phone_verification(self):
		url = reverse('accounts:phone_verification') 
		self.assertEqual(resolve(url).func.view_class, PhoneVerificationView)

	def test_sign_out(self):
		url = reverse('accounts:sign_out')
		self.assertEqual(resolve(url).func.view_class, SignOutView)

	def test_dashboard(self):
		url = reverse('accounts:dashboard', args=[1,])
		self.assertEqual(resolve(url).func.view_class, DashboardView)