from rest_framework.authentication import BasicAuthentication
from users.backends import EmailUsernameAuthentication as Eua
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _


class CustomBasicAuthentication(BasicAuthentication):
    def authenticate_credentials(self, userid, password, request=None):
        """
        Authenticate the userid and password against username and password
        with optional request for context.
        """
        if '@' in userid:
            user = Eua().authenticate(request, email=userid, password=password)
        else:
            user = Eua().authenticate(request, username=userid, password=password)
        if user is None:
            raise exceptions.AuthenticationFailed(_('Invalid username/password.'))

        if not user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))
        return (user, None)