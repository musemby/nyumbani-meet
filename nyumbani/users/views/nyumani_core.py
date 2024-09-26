import requests
import logging

from django.conf import settings
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework import response, permissions, serializers, status

from common.utils import parse_and_format_phone_number
from users.models import User
from users.serializers import (
    NyumbaniUserSerializer,
    NyumbaniLoginSerializer,
    UserSerializer,
    NyumbaniPasswordResetSerializer,
)
from users.models import User, NyumbaniUserSession
from organizations.models import Organization, UserOrganization

logger = logging.getLogger(__name__)


@api_view(["POST"])
def logout(request):
    Token.objects.filter(user=request.user).delete()
    return response.Response(status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def login(request):
    """
    POSTs to nyumbani core with phone number and default password.
    Nyumbani returns user details and token.
    If the `reset_password` field is True, the user is redirected to the password reset page.
    Password reset page POSTs to Nyumbani password reset endpoint. Then redirects to our log in page(use new password).
    Otherwise, the user is logged in and redirected to the app.
    Other Important details that Nyumbani returns are the roles of the user i.e Admin or Tenant
    We then save these details on our end and authenticate the user on our system.5t33qw
    """
    data = request.data
    serializer = NyumbaniLoginSerializer(data=data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data

    phone_number = data.get("phone_number", "")
    try:
        phone_number = parse_and_format_phone_number(phone_number)
    except ValidationError as e:
        message = f"Invalid phone number: {str(e)}"
        logger.error(message)
        return response.Response(
            {"message": message}, status=status.HTTP_400_BAD_REQUEST
        )
    
    stripped_phone_number = phone_number[1:]  # Remove the leading '+'

    password = data.get("password")
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    nyumbani_response = requests.post(
        f"{settings.NYUMBANI_LOGIN_URL}",
        json={"phone_number": stripped_phone_number, "password": password},
        headers=headers
    )

    if nyumbani_response.status_code != 200:
        nyumbani_response_error = nyumbani_response.json()
        logger.error(nyumbani_response_error)
        return response.Response(
            nyumbani_response_error, status=status.HTTP_400_BAD_REQUEST
        )
    
    nyumbani_response_data = nyumbani_response.json()['data']
    message = nyumbani_response_data['message']
    
    house_no = None
    payload = nyumbani_response_data['payload']
    metadata = payload['meta_data']
    role = metadata['role']
    if role == 'tenant':
        house_no = metadata['house']['house_no']

    reset_password = metadata['reset_password']
    organization = payload['organization']
    sub_organization = metadata.get('sub_organization')
    nyumbani_token = payload['token']
    user = payload['user']

    # create user 
    defaults = {
        "name": user['name'],
        "email": user['email'],
        "house_number": house_no,
        "nyumbani_role": role,
        "nyumbani_user_id": user['id'],
    }
    user, _ = User.objects.update_or_create(
        phone_number=phone_number,
        defaults=defaults
    )
    user.set_password(password)
    user.save()
    org_defaults = {
        "name": organization['name'],
    }
    org_obj, _ = Organization.objects.update_or_create(
        nyumbani_organization_id=organization['id'],
        defaults=org_defaults
    )
    if sub_organization:
        sub_org_defaults = {
            "name": sub_organization['name'],
        }
        sub_organization, _ = Organization.objects.update_or_create(
            nyumbani_organization_id=sub_organization['id'],
            parent=org_obj,
            defaults=sub_org_defaults
        )
    UserOrganization.objects.get_or_create(
        user=user,
        organization=org_obj,
        defaults={
            'is_admin':True if role == 'admin' else False
        }
    )

    NyumbaniUserSession.objects.update_or_create(
        user=user,
        defaults={
            "nyumbani_token": nyumbani_token,
        }
    )

    user = authenticate(username=phone_number,
                         password=password)

    if user is None:
        return response.Response(status=status.HTTP_401_UNAUTHORIZED)
    
    token, _ = Token.objects.get_or_create(user=user)
    user_serializer = UserSerializer(user)
    user_data = user_serializer.data
    user_data["token"] = token.key
    if reset_password:
        user_data['reset_password'] = True

    return response.Response(user_data, status=status.HTTP_200_OK)


@api_view(["POST"])
def password_reset(request):
    """
    POSTs to nyumbani core with phone number and new password.
    Nyumbani core updates the password and returns an updated user object.
    """
    user = request.user
    auth_token = request.auth

    data = request.data
    serializer = NyumbaniPasswordResetSerializer(data=data)
    serializer.is_valid(raise_exception=True)
 
    data = serializer.validated_data

    current_password = data.get("current_password")
    new_password = data.get("new_password")
    new_password_confirmation = data.get("new_password_confirmation")

    try:
        nyumbani_session = NyumbaniUserSession.objects.get(user=user)
    except NyumbaniUserSession.DoesNotExist:
        return response.Response(
            {"message": "No nyumbani session found"}, status=status.HTTP_404_NOT_FOUND
        )

    nyumbani_token = nyumbani_session.nyumbani_token
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {nyumbani_token}",
    }
    nyumbani_response = requests.post(
        f"{settings.NYUMBANI_PASSWORD_RESET_URL}",
        headers=headers,
        json={
            "current_password": current_password,
            "new_password": new_password,
            "new_password_confirmation": new_password_confirmation,
        }
    )
    print(nyumbani_response.content)
    if nyumbani_response.status_code != 200:
        nyumbani_response_error = nyumbani_response.json()
        return response.Response(
            nyumbani_response_error, status=status.HTTP_400_BAD_REQUEST
        )
    
    data = nyumbani_response.json()

    user.set_password(new_password)
    user.save()
    
    return response.Response(data, status=status.HTTP_200_OK)
