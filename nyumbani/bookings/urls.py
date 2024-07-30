from django.urls import path
from .views import (
    BookingsListApi,
    BookingsCreateApi,
    RoomsListApi,
    RoomsCreateApi,
    BookingsDeleteApi,
    BookingsUpdateApi,
    BuildingsListApi,
    BuildingsCreateApi,
    BuildingsDeleteApi,
)

urlpatterns = [
    path("bookings/", BookingsListApi.as_view(), name="bookings_list"),
    path("bookings/create/", BookingsCreateApi.as_view(), name="bookings_create"),
    path(
        "bookings/<uuid:pk>/delete/",
        BookingsDeleteApi.as_view(),
        name="bookings_delete",
    ),
    path(
        "bookings/<uuid:pk>/update/",
        BookingsUpdateApi.as_view(),
        name="bookings_update",
    ),
    path("rooms/", RoomsListApi.as_view(), name="rooms_list"),
    path("rooms/create/", RoomsCreateApi.as_view(), name="rooms_create"),
    path("buildings/", BuildingsListApi.as_view(), name="buildings_list"),
    path("buildings/create/", BuildingsCreateApi.as_view(), name="buildings_create"),
    path(
        "buildings/<uuid:pk>/delete/",
        BuildingsDeleteApi.as_view(),
        name="buildings_delete",
    ),
]
