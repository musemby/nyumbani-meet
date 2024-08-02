from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group, Permission

from common.serializers import UserActionMixin

from . import models

User = get_user_model()


class CreateUserSerializer(UserActionMixin):
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = (
            "name",
            "email",
            "phone_number",
            "house_number",
            "gender",
            "occupation",
            "id_number",
            "kra_pin",
            "password_reset_at",
            "nyumbani_role",
            "nyumbani_active",
        )
        extra_kwargs = {"password": {"write_only": True}}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)


class MeUserSerializer(serializers.ModelSerializer):
    profile_id = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            "firebase_uid",
            "display_name",
            "email",
            "phone_number",
            "interested_in",
            "experienced_seller",
            "weekly_target",
            "profile_id",
        )


# class UserProfileSerializer(serializers.ModelSerializer):

#     interested_in = serializers.ListField(allow_empty=True)

#     class Meta:
#         model = models.UserProfile
#         fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"


# ###########################################################################
# Nyumbani Core Serializers
# ###########################################################################


class NyumbaniLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()


class NyumbaniUserSerializer(serializers.Serializer):
    name = serializers.CharField()
    phone_number = serializers.CharField()
    house_number = serializers.CharField(
        allow_blank=True, allow_null=True, required=False
    )
    email = serializers.EmailField(allow_blank=True, allow_null=True, required=False)
    gender = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    occupation = serializers.CharField(
        allow_blank=True, allow_null=True, required=False
    )
    id_number = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    kra_pin = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    password_reset_at = serializers.DateTimeField(allow_null=True, required=True)


class NyumbaniLoginResponseSerializer(serializers.Serializer):
    name = serializers.CharField()
    phone_number = serializers.CharField()
    house_number = serializers.CharField()
    email = serializers