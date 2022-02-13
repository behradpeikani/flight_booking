from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, mobile_phone, password=None, **other_fields):
        if not mobile_phone:
            raise ValueError('Users must have phone number!')
        
        user = self.model(mobile_phone=mobile_phone, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, mobile_phone, password=None, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser muse have is_staff=True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser muse have is_superuser=True')
        return self.create_user(mobile_phone, password, **other_fields)



class User(AbstractUser):
    username = None
    mobile_phone = models.CharField(max_length=11, unique=True)
    otp = models.PositiveIntegerField(null=True, blank=True)
    otp_created = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'mobile_phone'
    REQUIRED_FIELDS = ()
    backend = 'accounts.authentication.MobileBackend' 




class Profile(models.Model):
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female')
        )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER, null=True, blank=True) 
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.user.mobile_phone