from django.contrib import admin

# Register your models here.

from .models import Booking, Building, Room

admin.site.register(Building)
admin.site.register(Room)
admin.site.register(Booking)
