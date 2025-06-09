from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    This can be used to add additional fields or methods in the future.
    """
    phone = models.IntegerField(unique=True, null=True, blank=True)
    is_theater_manager = models.BooleanField(default=False, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    otp = models.IntegerField(null=True, blank=True)
    otp_verified = models.BooleanField(default=False)

