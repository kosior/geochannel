from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from .models import WebSocket


def ws_exists(uuid, admin_key):
    return WebSocket.objects.filter(uuid=uuid, admin_key=admin_key).exists()


class WsTokenHeaderAuth(BaseAuthentication):
    keyword = 'Token'

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        ws_uuid = request.resolver_match.kwargs['uuid']

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(ws_uuid, token)

    def authenticate_credentials(self, ws_uuid, admin_key):
        if ws_exists(ws_uuid, admin_key):
            user = None
            auth = None
            return user, auth
        raise exceptions.AuthenticationFailed('Auth failed.')

    def authenticate_header(self, request):
        return self.keyword
