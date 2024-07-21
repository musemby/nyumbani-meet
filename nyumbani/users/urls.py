from django.urls import path

from rest_framework.routers import DefaultRouter

from . import views
from .views.users import UsersListApi, UsersDetailApi

router = DefaultRouter()
# router.register(r"users", views.UserViewSet, basename="users")
# # router.register(r"profiles", views.UserProfileViewSet, basename="profiles")
# router.register(r"groups", views.GroupViewSet, basename="groups")
# router.register(r"permissions", views.PermissionViewSet, basename="permissions")

urlpatterns = [
    path("nyumani_core/login/", views.login, name="login"),
    path("nyumani_core/password_reset/", views.password_reset, name="password_reset"),
    path("users/", UsersListApi.as_view(), name="users_list"),
    path("users/<str:pk>/", UsersDetailApi.as_view(), name="users_detail"),
]

urlpatterns += router.urls
