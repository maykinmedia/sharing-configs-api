from django.utils.translation import ugettext_lazy as _

from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication as _TokenAuthentication


class TokenAuthentication(_TokenAuthentication):
    def authenticate_credentials(self, key):
        from .models import ClientAuth

        try:
            token = ClientAuth.objects.get(token=key)
        except ClientAuth.DoesNotExist:
            raise exceptions.AuthenticationFailed(_("Invalid token."))

        return (None, token)
