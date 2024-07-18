from django.urls import path
from .views import BookingsListApi, BookingsCreateApi, RoomsListApi, RoomsCreateApi

urlpatterns = [
    path("bookings/", BookingsListApi.as_view(), name="bookings_list"),
    path("bookings/create/", BookingsCreateApi.as_view(), name="bookings_create"),
    path("rooms/", RoomsListApi.as_view(), name="rooms_list"),
    path("rooms/create/", RoomsCreateApi.as_view(), name="rooms_create"),
]
