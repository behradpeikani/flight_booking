from django.contrib.auth.backends import ModelBackend
from .models import User


class MobileBackend(ModelBackend):

	def authenticate(self, request, username=None, password=None, **kwargs):
		mobile_phone = kwargs['mobile_phone']
		try:
			user = User.objects.get(mobile_phone=mobile_phone)
		except User.DoesNotExist:
			pass