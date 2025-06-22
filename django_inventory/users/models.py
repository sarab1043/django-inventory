from django.db import models  
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager  
from django.utils.translation import gettext_lazy as _
 
# Create your models here.  
class CustomUser(AbstractUser):
    username=None
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    user_phone = models.CharField(max_length=20 , default=None, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
 
    object = CustomUserManager()

   
    def __str__(self):
        return self.email


class UserAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255, default=None)
    city = models.CharField(max_length=200, default=None)
    state = models.CharField(max_length=200, default=None)
    zipcode = models.IntegerField(default=None)
    street_address = models.TextField(default=None, null=True, blank=True)
    phone = models.IntegerField(default=None, null=True, blank=True)
    default = models.BooleanField(default=False)

    