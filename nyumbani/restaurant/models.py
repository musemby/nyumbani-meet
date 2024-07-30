from django.contrib.auth import get_user_model
from django.db import models

from organizations.models import AbstractOrganizationModel


class Restaurant(AbstractOrganizationModel):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Menu(AbstractOrganizationModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    file = models.FileField(upload_to="menus/", null=True, blank=True)
    is_active_menu = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["id", "organization"],
                condition=models.Q(is_active_menu=True),
                name="unique_active_menu_per_organization",
            ),
        ]
