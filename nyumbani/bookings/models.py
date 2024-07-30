from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError
from organizations.models import AbstractOrganizationModel

User = get_user_model()


class Building(AbstractOrganizationModel):
    name = models.CharField(max_length=255)
    number = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("organization", "name")


class Room(AbstractOrganizationModel):
    name = models.CharField(max_length=255)
    number = models.CharField(max_length=255, null=True, blank=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    capacity = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (("organization", "name", "building"),)


class Booking(AbstractOrganizationModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    booked_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="bookings"
    )
    booked_on = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField(null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        room_name = self.room.name if self.room else "No Room"
        booked_by_name = self.booked_by.name if self.booked_by else "No User"
        start_time = self.start_time.strftime("%Y-%m-%d %H:%M:%S")
        end_time = self.end_time.strftime("%Y-%m-%d %H:%M:%S")
        return f"{room_name} - {booked_by_name} - {start_time} - {end_time}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def validate(self):
        if self.room is None:
            raise ValidationError("Room is required")

        if self.start_time >= self.end_time:
            raise ValidationError("Start time must be before end time")

        # if there is an event that overlaps with this event
        if Booking.objects.filter(
            start_time__lte=self.end_time,
            end_time__gte=self.start_time,
            room=self.room,
        ).exists():
            raise ValidationError("There is an event at that time")
