from rest_framework import viewsets, status, response

from . import models, serializers


class AttachmentViewSet(viewsets.ModelViewSet):

    queryset = models.Attachment.objects.all()
    serializer_class = serializers.AttachmentSerializer
    filterset_fields = ['attachment_type']
