import copy
import uuid

from django.db import models

from django.contrib.auth.models import (
    Group, Permission, AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.contrib.postgres.fields import ArrayField
from phonenumber_field.modelfields import PhoneNumberField


GENDER_CHOICES = (
    ('MALE', 'MALE'),
    ('FEMALE', 'FEMALE'),
)

BOOLEAN_OPTIONS = (
    ('Yes', 'Yes'),
    ('No', 'No'),
)

class UserManager(BaseUserManager):

    def create_user(self, **fields):
        # import pdb; pdb.set_trace()
        user_fields = copy.copy(fields)
        password = user_fields.pop('password')
        user = self.model(**user_fields)
        user.set_password(password)
        user.is_active = True
        user.temp_pwd = password
        user.save(using=self._db)

        return user

    def create_superuser(self, **fields):
        user = self.create_user(**fields)
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):

    id = models.AutoField(primary_key=True)
    display_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255)
    phone_number = PhoneNumberField()
    business_name = models.CharField(max_length=15, null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    facebook = models.CharField(max_length=255, null=True, blank=True)
    instagram = models.CharField(max_length=255, null=True, blank=True)
    tiktok = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False, null=True, blank=True)
    dob = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES, null=True, blank=True)
    temp_pwd = models.CharField(max_length=255, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    @property
    def profile_id(self):
        return self.profile.id

    @property
    def interested_in(self):
        return self.profile.interested_in

    @property
    def experienced_seller(self):
        return self.profile.experienced_seller

    @property
    def weekly_target(self):
        return self.profile.weekly_target


class UserProfile(models.Model):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
