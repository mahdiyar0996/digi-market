from django.contrib.auth.hashers import check_password
from django.db.models import Q
from .models import User
from django.contrib import messages

class EmailUsernameAuthentication(object):
    @staticmethod
    def authenticate(request, email=None, username=None, password=None):
        try:
            user = User.objects.get(Q(username__exact=username) |
                                    Q(email__exact=email)
                                    )
        except User.DoesNotExist:
            return None
        if user.is_active == False:
            messages.error(request, 'حساب شما فعال نمی باشد', 'danger')
            return None
        if user and check_password(password, user.password):
            return user

        return None


