"""nyumbani URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path("admin/", admin.site.urls),
    # path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path("api-auth/", include("rest_framework.urls")),
    path("auth/", include("users.urls")),
    path("authorization/", include("djoser.urls")),
    path("authorization/", include("djoser.urls.authtoken")),
    path("common/", include("common.urls")),
    path("sentry-debug/", trigger_error),
    path("bookings/", include("bookings.urls")),
    path("restaurants/", include("restaurant.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
