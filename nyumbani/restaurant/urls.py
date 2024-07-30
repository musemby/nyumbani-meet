from django.urls import path
from .views import (
    RestaurantListApi,
    RestaurantCreateApi,
    RestaurantDeleteApi,
    RestaurantUpdateApi,
    MenuListApi,
    MenuCreateApi,
    MenuDeleteApi,
    MenuUpdateApi,
    MenuActiveRenderApi,
    MenuSetActiveApi,
)

urlpatterns = [
    path("restaurants/", RestaurantListApi.as_view(), name="restaurants_list"),
    path(
        "restaurants/create/", RestaurantCreateApi.as_view(), name="restaurants_create"
    ),
    path(
        "restaurants/<uuid:pk>/delete/",
        RestaurantDeleteApi.as_view(),
        name="restaurants_delete",
    ),
    path(
        "restaurants/<uuid:pk>/update/",
        RestaurantUpdateApi.as_view(),
        name="restaurants_update",
    ),
    path("menus/", MenuListApi.as_view(), name="menus_list"),
    path("menus/create/", MenuCreateApi.as_view(), name="menus_create"),
    path("menus/<uuid:pk>/delete/", MenuDeleteApi.as_view(), name="menus_delete"),
    path("menus/<uuid:pk>/update/", MenuUpdateApi.as_view(), name="menus_update"),
    path("menus/active/render/", MenuActiveRenderApi.as_view(), name="menus_active"),
    path(
        "menus/active/<uuid:pk>/set/",
        MenuSetActiveApi.as_view(),
        name="menus_set_active",
    ),
]
