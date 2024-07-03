from django.urls import path

from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='users')
router.register(r'profiles', views.UserProfileViewSet, basename='profiles')
router.register(r'groups', views.GroupViewSet, basename='groups')
router.register(r'permissions', views.PermissionViewSet, basename='permissions')

urlpatterns = [
    path('nyumani_core/login/', views.login, name='login'),
    path('nyumani_core/password_reset/', views.password_reset, name='password_reset'),
]

urlpatterns += router.urls
