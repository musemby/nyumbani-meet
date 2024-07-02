import requests

from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.db import transaction

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, permissions, serializers, viewsets, status, permissions

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework_simplejwt.tokens import RefreshToken

from common import mailer
from . import models, serializers

User = get_user_model()


def acquire_tokens_for_user(user):
    refresh_token = RefreshToken.for_user(user)

    return {
        'access_token': str(refresh_token.access_token),
        'refresh_token': str(refresh_token),
    }


def get_token(grant_type, username, password):
    r = requests.post(
        '{}/o/token/'.format(settings.AUTH_SERVER_URL),
        data={
            'grant_type': grant_type,
            'username': username,
            'password': password,
            'client_id': settings.CLIENT_ID,
            'client_secret': settings.CLIENT_SECRET,
        }
    )
    return Response(r.json())


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@transaction.atomic
def register(request):
    """Register users into the server and get an oauth token for them."""
    serializer = serializers.CreateUserSerializer(data=request.data) 
    if serializer.is_valid():
        serializer.save()
        # mailer.send_email(subject, message, recipients=[serializer.data['email']])
        return Response(data=serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        msg = "Please provide both the email and password to log in."
        return Response(data={"error": [msg]}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(email=email, password=password)
    if not user:
        msg = 'Invalid email and password combination.'
        return Response(data={"error": [msg]}, status=status.HTTP_400_BAD_REQUEST)

    tokens = acquire_tokens_for_user(user)

    return Response(data=tokens, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def me(request):
    # if request.user and request.user.is_authenticated:
    #     pass
    user = request.user
    ser = serializers.MeUserSerializer(user)
    data = ser.data
    return Response(data=data)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def token(request):
    """Get a token using username and password"""
    return get_token('password', request.data['email'], request.data['password'])


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def refresh_token(request):
    r = requests.post(
        '{}/o/token/'.format(settings.AUTH_SERVER_URL), 
        data={
            'grant_type': 'refresh_token',
            'refresh_token': request.data['refresh_token'],
            'client_id': settings.CLIENT_ID,
            'client_secret': settings.CLIENT_SECRET,
        },
    )
    return Response(r.json())


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def revoke_token(request):
    r = requests.post(
        '{}/o/revoke_token/'.format(settings.AUTH_SERVER_URL), 
        data={
            'token': request.auth,
            'client_id': settings.CLIENT_ID,
            'client_secret': settings.CLIENT_SECRET,
        },
    )
    if r.status_code == requests.codes.ok:
        return Response({'message': 'token revoked'}, r.status_code)
    return Response(r.json(), r.status_code)


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    filterset_fields = ['is_active', 'is_staff', 'gender']


class UserProfileViewSet(viewsets.ModelViewSet):

    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserProfileSerializer


class GroupViewSet(viewsets.ModelViewSet):

    queryset = models.Group.objects.all()
    serializer_class = serializers.GroupSerializer
    required_scopes = ['groups']


class PermissionViewSet(viewsets.ModelViewSet):

    queryset = models.Permission.objects.all()
    serializer_class = serializers.PermissionSerializer
