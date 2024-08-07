import copy
import uuid

from django.db import models

from django.contrib.auth.models import (
    Group,
    Permission,
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.contrib.postgres.fields import ArrayField
from phonenumber_field.modelfields import PhoneNumberField


GENDER_CHOICES = (
    ("MALE", "MALE"),
    ("FEMALE", "FEMALE"),
)

BOOLEAN_OPTIONS = (
    ("Yes", "Yes"),
    ("No", "No"),
)


class UserManager(BaseUserManager):
    def create_user(self, **fields):
        user_fields = copy.copy(fields)
        user = self.model(**user_fields)
        user.is_active = True
        user.save(using=self._db)

        if fields.get("password", None):
            user.set_password(fields["password"])
            user.save(using=self._db)

        return user

    def create_superuser(self, **fields):
        user = self.create_user(**fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone_number = PhoneNumberField(unique=True)
    house_number = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(
        max_length=255, choices=GENDER_CHOICES, null=True, blank=True
    )
    occupation = models.CharField(max_length=255, null=True, blank=True)
    id_number = models.CharField(max_length=255, null=True, blank=True)
    kra_pin = models.CharField(max_length=255, null=True, blank=True)
    password_reset_at = models.DateTimeField(null=True, blank=True)
    nyumbani_user_id = models.CharField(max_length=255, null=True, blank=True)
    nyumbani_role = models.CharField(max_length=255, null=True, blank=True)
    nyumbani_active = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "phone_number"

    def get_or_create_organization(self):
        from organizations.models import Organization, UserOrganization

        if UserOrganization.objects.filter(user=self).exists():
            return UserOrganization.objects.first(user=self).organization

        org = Organization.objects.create(name=f"{self.name}'s Organization")
        UserOrganization.objects.create(user=self, organization=org)
        return org

    @property
    def is_admin(self):
        return self.is_staff

    def is_organization_admin(self, organization):
        from organizations.models import UserOrganization

        org = organization
        parent_org = org.parent

        if UserOrganization.objects.filter(
            user=self, organization=org, is_admin=True
        ).exists():
            return True

        if (
            parent_org
            and UserOrganization.objects.filter(
                user=self, organization=parent_org, is_admin=True
            ).exists()
        ):
            return True

        return False

    def __str__(self) -> str:
        return f"{self.name} - {self.phone_number}"


class NyumbaniUserSession(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="nyumbani_user_sessions"
    )
    nyumbani_token = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
