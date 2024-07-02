from rest_framework import permissions
from rest_framework.authentication import BaseAuthentication
from users import exceptions
import firebase_admin
from firebase_admin import credentials, auth
from django.conf import settings

from django.contrib.auth import get_user_model

User = get_user_model()


"""SETUP FIREBASE CREDENTIALS"""
cred = credentials.Certificate({
    "type" : settings.FIREBASE_ACCOUNT_TYPE,
    "project_id" : settings.FIREBASE_PROJECT_ID,
    "private_key_id" : settings.FIREBASE_PRIVATE_KEY_ID,
    "private_key" : settings.FIREBASE_PRIVATE_KEY.replace('\\n', '\n'),
    "client_email" : settings.FIREBASE_CLIENT_EMAIL,
    "client_id" : settings.FIREBASE_CLIENT_ID,
    "auth_uri" : settings.FIREBASE_AUTH_URI,
    "token_uri" : settings.FIREBASE_TOKEN_URI,
    "auth_provider_x509_cert_url" : settings.FIREBASE_AUTH_PROVIDER_X509_CERT_URL,
    "client_x509_cert_url" : settings.FIREBASE_CLIENT_X509_CERT_URL
})
default_app = firebase_admin.initialize_app(cred)


class FirebaseAuthentication(BaseAuthentication):

    def authenticate(self, request):
        # Check if the view allows any user to access it
        if permissions.AllowAny in request.parser_context['view'].permission_classes:
            return None

        # import pdb; pdb.set_trace()
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            raise exceptions.NoAuthToken("No auth token provided")

        auth_header = auth_header.split(" ")[1]
        with open('token.txt', 'w') as f:
            f.write(auth_header)
        
        decoded_token = None
        try:
            decoded_token = auth.verify_id_token(auth_header)
        except Exception:
            raise exceptions.InvalidAuthToken("Invalid auth token")
        """Return Nothing"""
        # if not id_token or not decoded_token:
        #     return None
        """Get the uid of an user"""
        try:
            uid = decoded_token.get("uid")
        except Exception:
            raise exceptions.FirebaseError()
        
        user, created = User.objects.get_or_create(firebase_uid=uid)
        return (user, None)
