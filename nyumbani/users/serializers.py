from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group, Permission

from common.serializers import UserActionMixin

from . import models

User = get_user_model()


class CreateUserSerializer(UserActionMixin):

    display_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    phone_number = serializers.CharField(required=True)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('email', 'display_name', 'phone_number', 'password',)
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('password',)


class MeUserSerializer(serializers.ModelSerializer):

    profile_id = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'firebase_uid', 'display_name', 'email', 'phone_number',
            'interested_in', 'experienced_seller', 'weekly_target', 'profile_id'
        )


class UserProfileSerializer(serializers.ModelSerializer):

    interested_in = serializers.ListField(allow_empty=True)

    class Meta:
        model = models.UserProfile
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = '__all__'
