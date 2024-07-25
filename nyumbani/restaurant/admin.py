from django.contrib import admin

# Register your models here.

from .models import Restaurant, Menu

admin.site.register(Restaurant)
admin.site.register(Menu)
