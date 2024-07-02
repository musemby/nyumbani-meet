from django.conf import settings

from rest_framework import serializers

from . import models


class UserActionMixin(serializers.ModelSerializer):

    created_by = serializers.CharField(allow_null=True, required=False)
    
    def create(self, validated_data):
        request = self.context.get('request', {})
        if not request:
            return super().create(validated_data)

        validated_data['created_by'] = request.user.firebase_uid
        return super().create(validated_data)
        # TODO: updated_by population
    
    def to_representation(self, instance):
        fields = self.context['request'].query_params.get('fields', None)
        data = super().to_representation(instance)

        if fields:
            fields = fields.split(',')
            data = {k: v for k, v in data.items() if k in fields}

        return data


class AttachmentSerializer(UserActionMixin):

    class Meta:
        model = models.Attachment
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        domain = settings.API_DOMAIN
        full_path = domain + instance.file.url
        representation['file'] = full_path
        return representation
