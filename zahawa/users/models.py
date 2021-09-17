from django.db import models
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.postgres.fields import JSONField
from geolocation_fields.models import fields
# Model of Users


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True, blank=True, null=True)
    name = models.CharField(blank=True, null=True, max_length=100)
    profile_picture = models.ImageField(
        upload_to=None, null=True, blank=True, default=None
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    
    points = fields.PointField(blank=True, null=True, verbose_name="Point")
    phone_number = models.CharField(blank=True, null=True, max_length=100)
    verified = models.BooleanField(default=False)
    loyalty_program = models.PositiveIntegerField(default=0, null=True)    
    language = models.CharField(blank=True, null=True, max_length=100)
    promotion_notifications = models.BooleanField(default=False,null=True,blank=True)
    promotion_sms = models.BooleanField(default=False,null=True,blank=True)
    updates_notifications = models.BooleanField(default=False,null=True,blank=True)
    updates_sms = models.BooleanField(default=False,null=True,blank=True)
    orders_notifications = models.BooleanField(default=False,null=True,blank=True)
    orders_sms = models.BooleanField(default=False,null=True,blank=True)
    is_active = models.BooleanField(default=True,null=True,blank=True)
    is_staff = models.BooleanField(default=False,null=True,blank=True)
    is_superuser = models.BooleanField(default=False,null=True,blank=True)

    def __str__(self):
        if self.email:
            return self.email
        elif self.ip_addr:
            return self.ip_addr
        else:
            return ''



class Otp(models.Model):
    email = models.CharField(max_length=100)
    code = models.CharField(max_length=10)