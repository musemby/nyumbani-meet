from oauth2_provider.contrib.rest_framework import OAuth2Authentication
# from oauth2_provider.models import Application


class OAuth2ClientCredentialAuthentication(OAuth2Authentication):
    """
        Override default auth behaviour so as to set request.user for client app requests
    """

    def authenticate(self, request):
        authentication = super().authenticate(request)
        # import pdb; pdb.set_trace()
        # normal request by an actual user
        if authentication is not None:
            if not self.is_client_credential_request(authentication):
                return authentication

            # request by an app
            if self.is_client_credential_request(authentication):
                access_token = authentication[1]
                user = access_token.application.user
                return user, access_token

        return None

    def is_client_credential_request(self, authentication):
        access_token = authentication[1]
        return access_token.application.authorization_grant_type == Application.GRANT_CLIENT_CREDENTIALS
