from django.contrib.auth.hashers import check_password
from django.db.models import Q
from .models import User


class EmailUsernameAuthentication(object):
    @staticmethod
    def authenticate(request, email=None, username=None, password=None):
        try:
            user = User.objects.get(Q(username__exact=username)|
                                    Q(email__exact=email)
                                    )
        except User.DoesNotExist:
            return None

        if user and check_password(password, user.password):
            return user

        return None


