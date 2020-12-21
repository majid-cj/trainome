from django.contrib.auth.models import BaseUserManager
from django.db import models


class MemberManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password):
        user = self.model(first_name=first_name, last_name=last_name, email=email, password=password)
        user.set_password(password)
        user.is_active = True
        user.is_staff = False
        user.is_superuser = False
        user.member_type = 3
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password):
        user = self.model(first_name=first_name, last_name=last_name, email=email, password=password)
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.member_type = 1
        user.save(using=self._db)
        return

    def get_by_natural_key(self, email_):
        return self.get(email=email_)
