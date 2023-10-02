from django.db import models

from django.contrib.auth import get_user_model
from django.contrib.auth.models import (BaseUserManager,
                                        AbstractBaseUser,
                                        PermissionsMixin,)
from django.utils import timezone
from utils.validators import valid_email,valid_username, valid_phone_number, valid_password
from django.core.validators import RegexValidator
from django.forms.models import model_to_dict
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
        user.save()
        Profile.objects.create(user=user, first_name=username)
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
    username = models.CharField('نام کاربری', max_length=55, unique=True,null=True, validators=[valid_username()],
                                error_messages={'unique': 'کاربری با این نام وجود دارد',
                                                'invalid': 'نام کاربری باید از حروف,اعداد و ـ باشد'})
    email = models.EmailField('ایمیل' ,max_length=128, unique=True,null=True,
                              validators=[valid_email()],
                              error_messages={'unique': 'کاربری با این ایمیل وجود دارد',
                                              'invalid': 'لطفا یک ایمیل معتبر وارد کنید'})
    phone_number = models.CharField('شماره موبایل', max_length=20, unique=True, blank=True, null=True,
                                    validators=[valid_phone_number()],
                                    error_messages={'unique': 'این شماره قبلا انتخاب شده است',
                                                    'invalid': 'شماره وارد شده نا معتبر است'})
    credits = models.BigIntegerField('موجودی', null=True, blank=True)
    password = models.CharField('رمز عبور',max_length=255,
                                error_messages={'invalid': 'رمز کاربری باید ۸ کاراکتر یا بیشتر باشد و یک حرف بزرگ داشته باشد'})
    city = models.CharField('شهر',max_length=55, blank=True, null=True, db_index=True)
    address = models.TextField('ادرس', max_length=555, blank=True, null=True)
    is_superuser = models.BooleanField('ادمین', default=False, db_index=True)
    is_staff = models.BooleanField('کارکنان', default=False, db_index=True)
    ipaddress = models.GenericIPAddressField('ایپی ادرس', blank=True, null=True, db_index=True)
    last_password_reset = models.DateTimeField(null=True, blank=True)
    objects = UserManager()
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']
    date_joined = None
    first_name = None
    last_name = None
    class Meta:
        db_table = 'users'
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['created_at']


    def __str__(self):
        return self.username

    def active_users(self):
        return self.objects.filter(is_active=True)

    def to_dict(self):
        return model_to_dict(self)

    def get_model_fields(self):
        return self._meta.get_fields()
    def save(self, *args, **kwargs):
        self.username = kwargs.get('username', self.username)
        self.email = kwargs.get('email', self.email)
        self.phone_number = kwargs.get('phone_number', self.phone_number)
        self.city = kwargs.get('city', self.city)
        self.address = kwargs.get('address', self.address)
        super().save()

class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, related_name='%(class)s', blank=True, on_delete=models.CASCADE)
    avatar = models.ImageField('اواتار', blank=True, null=True, upload_to='media/users/profile/',
                               default='users/profile/default.jpg')
    first_name = models.CharField('نام', max_length=55, null=True, blank=True)
    last_name = models.CharField('نام خانوادگی', max_length=55, blank=True, null=True)
    age = models.SmallIntegerField('تاریخ تولد', blank=True, null=True)
    job = models.CharField('شغل', blank=True, null=True, max_length=55)
    updated_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'users-profiles'
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'


    def __str__(self):
        return self.user.username

    def to_dict(self):
        return model_to_dict(self)

    def get_model_fields(self):
        return self._meta.get_fields()
    
    def save(self, *args, **kwargs):
        self.first_name = kwargs.get('first_name', self.first_name)
        self.last_name = kwargs.get('last_name', self.last_name)
        self.age = kwargs.get('age', self.age)
        self.job = kwargs.get('job', self.job)
        super().save()

class UserBasket(models.Model):
    product = models.ForeignKey('products.Product', verbose_name='کالا', unique=True, related_name='%(class)s', on_delete=models.CASCADE, db_index=True)
    user = models.ForeignKey(User, related_name='%(class)s', on_delete=models.CASCADE, db_index=True)
    count = models.SmallIntegerField(verbose_name='تعداد', blank=True, default=1)


    class Meta:
        db_table = 'users-basket'
        verbose_name = 'basket'
        verbose_name_plural = 'baskets'