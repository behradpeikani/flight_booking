from django import forms
from .models import User, Profile


class SignUpForm(forms.ModelForm):
	
	class Meta:
		model = User
		fields = ('mobile_phone',)


# class PhoneVerificationForm(forms.Form):
# 	code = forms.IntegerField()


class ProfileForm(forms.ModelForm):

	class Meta:
		model = Profile
		fields = ('first_name', 'last_name', 'gender', 'email')
