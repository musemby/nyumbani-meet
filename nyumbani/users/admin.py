from django.contrib import admin

# Register your models here.

from .models import User, NyumbaniUserSession

admin.site.register(User)
admin.site.register(NyumbaniUserSession)
