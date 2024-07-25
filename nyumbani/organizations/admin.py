from django.contrib import admin

# Register your models here.

from .models import Organization, UserOrganization

admin.site.register(Organization)
admin.site.register(UserOrganization)
