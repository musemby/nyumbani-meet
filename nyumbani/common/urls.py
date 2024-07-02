from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'attachments', views.AttachmentViewSet, basename='attachments')

urlpatterns = router.urls
