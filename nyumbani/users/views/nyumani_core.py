import requests

from django.conf import settings
from django.contrib.auth import authenticate

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework import response, permissions, serializers, status
from nyumbani.users.serializers import (
    NyumbaniUserSerializer,
    NyumbaniLoginSerializer,
    UserSerializer
)


@api_view(['POST'])
def login(request):
    """
    POSTs to nyumbani core with phone number and default password.
    Nyumbani returns user details and token.
    If the `password_reset_at` field is not None, the user is redirected to the password reset page.
    Otherwise, the user is logged in and redirected to the app.
    Other Important details that Nyumbani returns are the roles of the user i.e Admin or Tenant
    We then save these details on our end and authenticate the user on our system.
    """
    data = request.data
    serializer = NyumbaniLoginSerializer(data=data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data

    phone_number = data.get('phone_number')
    password = data.get('password')

    response = requests.post(
        f'{settings.NYUMBANI_LOGIN_URL}',
        json={
            'phone_number': phone_number,
            'password': password
        }
    )

    response_serializer = NyumbaniUserSerializer(data=response.json())
    response_serializer.is_valid(raise_exception=True)
    response_data = response_serializer.validated_data

    password_reset_at = response_data.get('password_reset_at')
    
    if password_reset_at:
        return response.Response(
            {
                'message': 'Password reset required',
                'user': response_data
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=phone_number, password=password)
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user)
        user_data = user_serializer.data
        user_data['token'] = token.key
        return response.Response(user_data, status=status.HTTP_200_OK)
    else:
        return response.Response(status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['POST'])
def password_reset(request):
    """
    POSTs to nyumbani core with phone number and new password.
    Nyumbani core updates the password and returns an updated user object.
    """
    data = request.data
    serializer = NyumbaniLoginSerializer(data=data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data

    phone_number = data.get('phone_number')
    password = data.get('password')

    response = requests.post(
        f'{settings.NYUMBANI_PASSWORD_RESET_URL}',
        json={
            'phone_number': phone_number,
            'password': password
        }
    )

    response_serializer = NyumbaniUserSerializer(data=response.json())
    response_serializer.is_valid(raise_exception=True)
    response_data = response_serializer.validated_data

    return response.Response(response_data, status=status.HTTP_200_OK)
