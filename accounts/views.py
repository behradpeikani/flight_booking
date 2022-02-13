from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import SignUpForm, ProfileForm
from .models import User, Profile
from . import helper
from django.views import View
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import AnonymousRequiredMixin # Mixin that will redirect authenticated users to a different view.


class SignUpView(AnonymousRequiredMixin, View):
	form_class = SignUpForm
	template_name = 'accounts/sign_up.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class
		user = User.objects.all()
		return render(request, self.template_name, {"form": form, "user": user})

	def post(self, request, *args, **kwarsg):
		form = self.form_class(request.POST or None)

		try:
			# sign in
			if "mobile_phone" in request.POST:
				mobile_phone = request.POST.get('mobile_phone')
				user = User.objects.get(mobile_phone=mobile_phone)
				otp = helper.get_random_otp()
				helper.send_otp_soap(mobile_phone, otp)
				print(otp)
				user.otp = otp
				user.save()
				request.session['user_mobile'] = user.mobile_phone
				messages.success(request, 'Please verify your phone number.', 'success')
				return redirect('accounts:phone_verification')
			else:
				messages.error(request, 'Invalid phone number!', 'warning')

		except User.DoesNotExist:
			# sign up
			form = self.form_class(request.POST or None)
			if form.is_valid():
				user = form.save(commit=False)
				mobile_phone = request.POST.get('mobile_phone')
				otp = helper.get_random_otp()
				helper.send_otp_soap(mobile_phone, otp)
				print(otp)
				user.otp = otp
				user.is_active = False
				user.save()
				request.session['user_mobile'] = user.mobile_phone
				messages.success(request, 'Please verify your phone number.', 'success')
				return redirect('accounts:phone_verification')
			else:
				messages.error(request, 'Invalid phone number!', 'warning')

		return render(request, self.template_name, {"form": form})


class PhoneVerificationView(AnonymousRequiredMixin, View):
	template_name = 'accounts/phone_verification.html'

	def get(self, request, *args, **kwargs):
		mobile_phone = request.session.get('user_mobile')
		user = User.objects.get(mobile_phone = mobile_phone)
		return render(request, self.template_name)  

	def post(self, request, *args, **kwargs):
		try:
			mobile_phone = request.session.get('user_mobile')
			user = User.objects.get(mobile_phone=mobile_phone)
			if not helper.check_otp_expiration(user.mobile_phone):
				messages.error(request, "Code is expired, please try again.")
				return redirect('accounts:sign_up')

			if user.otp != int(request.POST.get('otp')):
				messages.error(request, "Invalid code!")

			user.is_active = True
			user.save()
			login(request, user)
			return redirect('flights:search_flight')
			return render(request, self.template_name, {"mobile_phone": mobile_phone})

		except User.DoesNotExist:
			messages.error(request, "Error, try again.")
			return redirect('accounts:sign_up')


class SignOutView(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		logout(request)
		messages.info(request, 'You logged out!', 'info')
		return redirect('flights:home')


class DashboardView(LoginRequiredMixin, View):
	template_name = 'accounts/dashboard.html'
	form_class = ProfileForm

	def get(self, request, pk, *args, **kwargs):
		user = get_object_or_404(User, pk=pk)
		Profile.objects.get_or_create(user=request.user)
		form = self.form_class
		return render(request, self.template_name, {"user": user, "form": form})

	def post(self, request, pk, *args, **kwargs):
		form = self.form_class(request.POST, instance=request.user.profile)
		if form.is_valid():
			form.save()
			messages.success(request, 'Profile created successfully.', 'success')
			return redirect('accounts:dashboard', request.user.pk)

		return render(request, self.template_name, {"form": form})


