from random import randint

from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from rest_framework.authtoken.models import Token
from django.shortcuts import reverse
from .managers import MemberManager


# Create your models here.

error_msg = _('user name should only contains white spaces, and minimum three characters')

class Member(PermissionsMixin, AbstractBaseUser):
    ADMIN = 1
    MANAGER = 2
    END_USER = 3
    OPTIONS = (
        (ADMIN, _('System Admin')),
        (MANAGER, _('Sub Admins')),
        (END_USER, _('End User')),)
    member_type = models.IntegerField(choices=OPTIONS, default=ADMIN)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']
    USERNAME_FIELD = 'email'

    objects = MemberManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email}"

    def get_short_name(self):
        return f"{self.first_name} {self.last_name}"

    def natural_key(self):
        return f"{self.first_name} {self.last_name}"

    def get_auth_token(self):
        return Token.objects.get(user=self)

    def get_absolute_url(self):
        return reverse("home:index")

    def check_is_superuser(self):
        return self.is_superuser
