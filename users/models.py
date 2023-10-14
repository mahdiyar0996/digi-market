from django.db import models
from django.db.models import F
from django.contrib.auth.models import (BaseUserManager,
                                        AbstractBaseUser,
                                        PermissionsMixin,)
from utils.validators import valid_email,valid_username, valid_phone_number, valid_password
from django.forms.models import model_to_dict
from django_redis import get_redis_connection
import json
from django.core.cache import cache as django_cache

cache = get_redis_connection('default')


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
    username = models.CharField('نام کاربری', max_length=55, unique=True, validators=[valid_username()],
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
    password = models.CharField('رمز عبور', max_length=255,
                                error_messages={'invalid': 'رمز کاربری باید ۸ کاراکتر یا بیشتر باشد و یک حرف بزرگ داشته باشد'})
    city = models.CharField('شهر', max_length=55, blank=True, null=True,  db_index=True)
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
    avatar = models.ImageField('اواتار', blank=True, null=True, upload_to='users/profile/',
                               default='users/profile/default.jpg')
    first_name = models.CharField('نام', max_length=55, blank=True, null=True)
    last_name = models.CharField('نام خانوادگی', max_length=55, blank=True, null=True)
    age = models.SmallIntegerField('تاریخ تولد', blank=True, null=True)
    job = models.CharField('شغل', blank=True, max_length=55, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

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

    @classmethod
    def get_user_and_profile(cls, request, user: User):
        profile = cls.objects.select_related('user').values('avatar', 'first_name', 'last_name', 'job', 'age',
                                                              'user__username', 'user__email', 'user__phone_number',
                                                              'user__credits', 'user__city', 'user__address',
                                                              'user__address').get(user=user)
        profile['avatar'] = request.build_absolute_uri("/media/" + profile['avatar'])
        # user_data = {key.replace('user__', ''): value for key, value in profile.items() if 'user' in key}
        profile_copy = profile.copy()
        user_data = {}
        for key, value in profile_copy.items():
            if 'user' in key:
                user_data[key.replace('user__', '')] = value
                profile.pop(key)
        with cache.pipeline() as pipeline:
            pipeline.hset(f'user{user.id}', mapping=user_data)
            pipeline.expire(f"user{user.id}", 7200)
            pipeline.hset(f'profile{user.id}', mapping=profile)
            pipeline.expire(f"profile{user.id}", 7200)
            pipeline.execute()
        return user_data, profile


class UserBasket(models.Model):
    product = models.OneToOneField('products.Product', verbose_name='کالا', related_name='%(class)s', on_delete=models.CASCADE, db_index=True)
    profile = models.ForeignKey(Profile, related_name='%(class)s', on_delete=models.CASCADE, db_index=True)
    count = models.SmallIntegerField(verbose_name='تعداد', blank=True, default=1)


    class Meta:
        db_table = 'users-basket'
        verbose_name = 'basket'
        verbose_name_plural = 'baskets'

    @classmethod
    def filter_basket_products(cls, request, user: User):
        products = cls.objects.select_related('product', 'profile', 'profile__user').\
            values('product__category__name', 'product__avatar', 'product__name', 'product__details',
                   'product__stock', 'product__price', 'product__warranty', 'count',
                   'product__id').\
            filter(profile__user=user)
        # pipeline = cache.pipeline()
        for item in products:
            item['product__avatar'] = request.build_absolute_uri("/media/" + item['product__avatar'])
            item['product__price'] = "{:,}".format(item['product__price'])
        django_cache.set(f'user_basket{user.id}', products, 60)
        # pipeline.hset(f'user_basket{user.id}', mapping=item)
        # pipeline.expire(f'user_basket{user.id}', 7200)
        # pipeline.execute()
        return products

    @classmethod
    def get_basket_product_counts(cls, user, product_id):
        products = cls.objects.select_related('product',). \
            values('count').get(profile__user__username=user, product__id=product_id)
        return products