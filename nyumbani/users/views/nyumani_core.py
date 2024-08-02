import requests

from django.conf import settings
from django.contrib.auth import authenticate

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework import response, permissions, serializers, status
from users.models import User
from users.serializers import (
    NyumbaniUserSerializer,
    NyumbaniLoginSerializer,
    UserSerializer,
)
from users.models import User, NyumbaniUserSession
from organizations.models import Organization, UserOrganization


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
    if phone_number:
        if not phone_number.startswith('+'):
            phone_number = '+' + phone_number
        stripped_phone_number = phone_number[1:]  # Remove the leading '+'
        
    password = data.get("password")

    nyumbani_response = requests.post(
        f"{settings.NYUMBANI_LOGIN_URL}",
        json={"phone_number": stripped_phone_number, "password": password},
    )

    message = "An error occurred while logging in. Please try again later."

    if nyumbani_response.status_code != 200:
        return response.Response(
            {"message": message}, status=response.status_code
        )
    message = nyumbani_response.json()['data']['message']

    house_no = None
    payload = nyumbani_response.json()['data']['payload']
    metadata = payload['meta_data']
    role = metadata['role']
    if role == 'tenant':
        house_no = metadata['house']['house_no']

    reset_password = metadata['reset_password']
    organization = payload['organization']
    sub_organization = metadata.get('sub_organization')
    nyumbani_token = payload['token']
    user = payload['user']
    
    if reset_password:
        return response.Response(
            {"message": "Password reset required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # create user 
    defaults = {
        "name": user['name'],
        "email": user['email'],
        "house_number": house_no,
        "nyumbani_role": role,
        "nyumbani_user_id": user['id'],
    }
    user, _ = User.objects.get_or_create(
        phone_number=phone_number,
        defaults=defaults
    )
    user.set_password(password)
    user.save()

    organization, _ = Organization.objects.get_or_create(
        name=organization['name'],
    )
    if sub_organization:
        sub_organization, _ = Organization.objects.get_or_create(
            name=sub_organization['name'],
            parent=organization
        )
    user_org, _ = UserOrganization.objects.get_or_create(
        user=user,
        organization=organization,
        defaults={
            'is_admin':True if role == 'admin' else False
        }
    )

    import pdb; pdb.set_trace()

    NyumbaniUserSession.objects.get_or_create(
        user=user,
        nyumbani_token=nyumbani_token
    )

    user = authenticate(username=phone_number,
                         password=password)

    # user = User.objects.get(phone_number=phone_number)

    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user)
        user_data = user_serializer.data
        user_data["token"] = token.key
        return response.Response(user_data, status=status.HTTP_200_OK)
    else:
        return response.Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
def password_reset(request):
    """
    POSTs to nyumbani core with phone number and new password.
    Nyumbani core updates the password and returns an updated user object.
    """
    data = request.data
    serializer = NyumbaniLoginSerializer(data=data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data

    phone_number = data.get("phone_number")
    password = data.get("password")

    nyumbani_response = requests.post(
        f"{settings.NYUMBANI_PASSWORD_RESET_URL}",
        json={"phone_number": phone_number, "password": password},
    )

    response_serializer = NyumbaniUserSerializer(data=nyumbani_response.json())
    response_serializer.is_valid(raise_exception=True)
    response_data = response_serializer.validated_data

    return response.Response(response_data, status=status.HTTP_200_OK)
