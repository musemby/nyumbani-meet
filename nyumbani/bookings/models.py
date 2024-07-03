from django.contrib.auth import get_user_model
from django.db import models

from organizations.models import AbstractOrganizationModel

User = get_user_model()


class Building(AbstractOrganizationModel):

    name = models.CharField(max_length=255)
    number = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name


class Room(AbstractOrganizationModel):
    
    name = models.CharField(max_length=255)
    number = models.CharField(max_length=255, null=True, blank=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    capacity = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name


class Booking(AbstractOrganizationModel):

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    booked_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='bookings')
    booked_on = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.room.name