from django.db import models

from common.models import AbstractBase


class Organization(AbstractBase):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class AbstractOrganizationModel(AbstractBase):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class UserOrganization(AbstractOrganizationModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
