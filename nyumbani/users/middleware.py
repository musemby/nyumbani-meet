from urllib.parse import parse_qs
from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

User = get_user_model()


@database_sync_to_async
def get_user_from_token(token_key):
    org_member = None
    organization = None
    role = None
    try:
        access_token = AccessToken(token_key)
        user = User.objects.get(id=access_token['user_id'])
        org_member = user.org_members.first()
        if org_member:
            organization = org_member.organization
            role = org_member.role
    except Exception as exception:
        print(exception)
        user = AnonymousUser()
    finally:
        close_old_connections()
    
    return org_member, user, organization, role


class TokenAuthMiddleware:

    """Auth middleware for django channels connections"""

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        params = parse_qs(scope['query_string'])
        token = params.get(b'token')[0].decode()
        org_member, user, org, role = await get_user_from_token(token)
        scope['user'] = user
        scope['organization'] = org
        scope['role'] = role
        scope['org_member'] = org_member

        return await self.inner(scope, receive, send)

TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
