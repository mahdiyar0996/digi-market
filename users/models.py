from django.db import models

from django.contrib.auth import get_user_model
from django.contrib.auth.models import (BaseUserManager,
                                        AbstractBaseUser,
                                        PermissionsMixin,)
from django.utils import timezone
from utils.validators import valid_email,valid_username, valid_phone_number, valid_password
from django.core.validators import RegexValidator
class AbstractBase(models.Model):
    created_at = models.DateTimeField(auto_now=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, username, email, password, is_superuser, is_staff, is_active, **kwargs):
        if username is None:
            username = email.split('@')[0]

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **kwargs)
        user.is_superuser = is_superuser
        user.is_staff = is_staff
        user.is_active = is_active
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password,
                    is_superuser=False, is_staff=False, is_active=True, **kwargs):
        return self._create_user(username, email, password, is_superuser=is_superuser,
                                 is_staff=is_staff, is_active=is_active, **kwargs)

    def create_superuser(self, username, email, password,
                         is_superuser=True, is_staff=True, is_active=True, **kwargs):
        return self._create_user(username, email, password, is_superuser=is_superuser,
                                 is_staff=is_staff, is_active=is_active, **kwargs)





class User(AbstractBaseUser, PermissionsMixin, AbstractBase):
    username = models.CharField(max_length=55, unique=True, validators=[valid_username()],
                                error_messages={'unique': 'کاربری با این نام وجود دارد',
                                                'invalid': 'نام کاربری باید از حروف,اعداد و ـ باشد'})
    email = models.EmailField(max_length=128, unique=True,
                              validators=[valid_email()],
                              error_messages={'unique': 'کاربری با این ایمیل وجود دارد',
                                              'invalid': 'لطفا یک ایمیل معتبر وارد کنید'})
    phone_number = models.CharField(max_length=20, unique=True, blank=True, null=True,
                                    validators=[valid_phone_number()],
                                    error_messages={'unique': 'این شماره قبلا انتخاب شده است',
                                                    'invalid': 'شماره وارد شده نا معتبر است'})
    first_name = models.CharField(max_length=55, null=True, blank=True)
    last_name = models.CharField(max_length=55, blank=True, null=True)
    city = models.CharField(max_length=55, blank=True, null=True, db_index=True)
    address = models.TextField(max_length=555, blank=True, null=True)
    is_superuser = models.BooleanField(default=False, db_index=True)
    is_staff = models.BooleanField(default=False, db_index=True)
    ipaddress = models.GenericIPAddressField(blank=True, null=True, db_index=True)
    last_password_reset = models.DateTimeField(null=True, blank=True)
    objects = UserManager()
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']
    date_joined = None
    class Meta:
        db_table = 'users'
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['created_at']


    def __str__(self):
        return self.username

    def active_users(self):
        return self.objects.filter(is_active=True)
