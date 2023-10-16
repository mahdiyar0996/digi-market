import json
import pickle
import string

from django.db import models
from .managers import ProductManager
from django.db.models import Sum, Count, F, Avg, Max
from main.settings import cache
from django.core.cache import cache as django_cache
from utils.tools import get_discount

class BaseAbstract(models.Model):
    name = models.CharField("نام", max_length=255)
    created_at = models.DateTimeField('تاریخ انتشار', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ آخرین اپدیت', auto_now=True)
    class Meta:
        abstract = True


class Category(BaseAbstract):
    avatar = models.ImageField("آواتار", upload_to='products/category/avatar/')

    def __str__(self):
        return self.name
    class Meta:
        db_table = "categories"
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class SubCategory(BaseAbstract):
    category = models.ForeignKey(Category,verbose_name='مجموعه', related_name='%(class)s',
                                 on_delete=models.DO_NOTHING, db_index=True)
    name = models.CharField("نام", max_length=255, db_index=True)
    avatar = models.ImageField("آواتار", upload_to='products/subcategory/avatar/')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "sub_categories"
        verbose_name = 'sub_category'
        verbose_name_plural = 'sub_categories'

    @classmethod
    def all_categories_and_subcategories(cls, request):
        subcategory = cls.objects.select_related('category').all()
        category = []
        for item in subcategory:
            if item.category not in category:
                item.category.avatar = request.build_absolute_uri(item.category.avatar.url)
                category.append(item.category)
            item.avatar = request.build_absolute_uri(item.avatar.url)
        django_cache.set('category', category)
        django_cache.set('subcategory', subcategory)
        return category, subcategory

    @classmethod
    def filter_subcategory_with_category(cls,request ,category_name):
        subcategory = cls.objects.filter(category__name__exact=category_name).values('name', 'avatar')
        for item in subcategory:
            item['avatar'] = request.build_absolute_uri('/media/' + item['avatar'])
        django_cache.set(f'list_of_subcategories{category_name}', subcategory, 60 * 5)
        return subcategory


class SubSubCategory(BaseAbstract):
    category = models.ForeignKey(SubCategory, related_name='%(class)s',
                                 verbose_name='مجموعه', on_delete=models.DO_NOTHING, db_index=True)
    name = models.CharField("نام", max_length=255, db_index=True)
    avatar = models.ImageField(blank=True, null=True, upload_to='products/subsubcategory')
    brand = models.JSONField("برند", blank=True, null=True)
    details = models.JSONField("جزییات", blank=True, null=True)

    class Meta:
        db_table = 'sub-sub-categories'
        verbose_name = 'sub_sub_category'
        verbose_name_plural = 'sub_sub_categories'

    def __str__(self):
        return self.name

    @classmethod
    def filter_categories_with_category_list(cls, request, subcategories, category_name):
        subcategory_list = [i['name'] for i in subcategories]
        sub_sub_category = cls.objects.values('name', 'avatar').filter(category__name__in=subcategory_list)
        for item in sub_sub_category:
            item['avatar'] = request.build_absolute_uri('/media/' + item['avatar'])
        django_cache.set(f'sub_sub_categories{category_name}', sub_sub_category, 60 * 10)
        return sub_sub_category

    @classmethod
    def all_sub_categories_with_products(cls, request, categories):
        if len(categories) > 0:
            sub_sub_categories = cls.objects.prefetch_related('product').filter(name__in=categories)[:4][:4]
        else:
            sub_sub_categories = cls.objects.prefetch_related('product').all()[:4]
        # for item in sub_sub_categories:
        #     for product in item.product.all()[:4]:
        #         product.avatar = request.build_absolute_uri("/media/" + product.avatar)
        ipaddress = request.META.get('REMOTE_ADDR')
        django_cache.set(f'user_recent_products{ipaddress}', sub_sub_categories, 60 * 10)
        return sub_sub_categories


class Product(BaseAbstract):
    category = models.ForeignKey(SubSubCategory, verbose_name='مجموعه', related_name='%(class)s', on_delete=models.DO_NOTHING)
    brand = models.CharField("برند", max_length=55, blank=True, null=True)
    description = models.TextField("درباره کالا", max_length=1000, blank=True, null=True)
    details = models.JSONField("جزییات", blank=True, null=True)
    warranty = models.CharField("گارانتی", max_length=255, blank=True)
    price = models.BigIntegerField("قیمت",)
    discount = models.IntegerField('تخفیف', blank=True, default=0)
    is_active = models.BooleanField('وضعیت', default=True, db_index=True)
    colour = models.CharField("رنگ", max_length=55, blank=True,)
    stock = models.BigIntegerField("تعداد کالا", blank=True, null=True)
    avatar = models.ImageField('آواتار', blank=True, upload_to='products/avatar/')
    objects = ProductManager

    class Meta:
        db_table = 'products'
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ['created_at', 'stock', 'price']

    def get_discount(self):
        discount = self.price * self.discount // 100
        discounted_price = self.price - discount
        price = "{:,}".format(int(discounted_price))
        return price

    def split_price(self):
        price = "{:,}".format(self.price)
        return price

    def __str__(self):
        return self.name

    @classmethod
    def filter_products_with_sub_category(cls, request, category_name):
        products = cls.objects.select_related('category').filter(category__name__exact=category_name).order_by('category__name')
        for item in products:
            item.avatar = request.build_absolute_uri('/media/' + item.avatar)
        django_cache.set(f'list_of_subcategories_products{category_name}', products, 60 * 5)
        return products

    @classmethod
    def filter_product_with_sub_sub_category(cls, request, category_name):
        products = Product.objects.select_related('category').annotate(
            average=Avg('productcomment__rating'), max_price=Max('price')).values('category__name',
            'name', 'id', 'avatar', 'price', 'discount','details','max_price',
            'stock', 'average').filter(category__category__name=category_name)
        sub_sub_categories = set()
        for item in products:
            sub_sub_categories.add(item['category__name'])
            item['avatar'] = request.build_absolute_uri('/media/' + item['avatar'])
            item['discounted_price'] = '{:,}'.format(get_discount(item['price'], item['discount']))
            item['price'] = '{:,}'.format(item['price'])
        django_cache.set(f'sub_sub_categories{category_name}', sub_sub_categories, 60 * 10)
        django_cache.set(f'products_{category_name}', products, 60 * 10)
        return products, sub_sub_categories

    @classmethod
    def filter_products_and_get_sub_sub_categories(cls, request, category_name):
        products = cls.objects.select_related('category').annotate(
            average=Avg('productcomment__rating'), max_price=Max('price')).values('category__name','category__brand',
                                                                                  'category__details',
                                                                                  'name', 'id', 'avatar', 'price',
                                                                                  'discount', 'details', 'max_price',
                                                                                  'stock', 'average', ).filter(
            category__name=category_name)
        for item in products:
            item['avatar'] = request.build_absolute_uri('/media/' + item['avatar'])
            item['discounted_price'] = '{:,}'.format(get_discount(item['price'], item['discount']))
            item['price'] = '{:,}'.format(item['price'])
        django_cache.set(f'products_{category_name}', products, 60 * 10)
        return products


    @classmethod
    def filter_product_with_most_discount(cls, request, discount, **kwargs):
        category = kwargs.get('category__name')
        if category == 'home':
            del kwargs['category__name']
        products = cls.objects.select_related('category').values('category__name',"id",'avatar', "name",
                                                                     "price", 'discount').filter(**kwargs)[:18]
        for item in products:
            item['avatar'] = request.build_absolute_uri('/media/' + item['avatar'])
            item['discounted_price'] = "{:,}".format( item['price'] - (item['price'] * item['discount'] // 100))
            item['price'] = '{:,}'.format(item['price'])
        django_cache.set(f'discounted_products{category}', products, 60 * 10)
        return products

class ProductImage(models.Model):
    product = models.ForeignKey(Product,verbose_name='کالا', related_name='%(class)s', on_delete=models.CASCADE, db_index=True)
    images = models.ImageField('عکس ها', upload_to='products/images/', blank=True)

    class Meta:
        db_table = 'products_images'
        verbose_name = 'product_image'
        verbose_name_plural = 'products_images'

    def __str__(self):
        return self.product.name

    @classmethod
    def get_product_and_images(cls, request, product_id):
        images = cls.objects.select_related(
            'product', 'product__category',
            'product__category',
            'product__category__category','product__category__category__category').filter(product_id=product_id)
        print(images)
        product = images[0].product
        for item in images:
            item.images = request.build_absolute_uri(item.images.url)
        django_cache.set(f'product:{product_id}', product, 60 * 10)
        django_cache.set(f'images:{product_id}', images, 60 * 10)
        return product, images


class ProductComment(BaseAbstract):
    choices = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]
    product = models.ForeignKey(Product,verbose_name='کالا', related_name='%(class)s', on_delete=models.CASCADE, db_index=True)
    user = models.ForeignKey('users.User', related_name='%(class)s', on_delete=models.CASCADE, db_index=True)
    rating = models.SmallIntegerField("امتیاز", choices=choices, db_index=True)
    comment = models.TextField('دیدگاه')
    is_active = models.BooleanField('وضعیت', default=False, db_index=True)
    name = None

    class Meta:
        db_table = 'products_comments'
        verbose_name = 'product-comment'
        verbose_name_plural = 'products_comments'
        ordering = ['rating', 'updated_at', 'created_at']

    def __str__(self):
        return self.user.username

    @staticmethod
    def is_active_comments(product_id):
        comments = ProductComment.objects.select_related('user').filter(product__id=product_id)
        django_cache.set(f'comments:{product_id}', comments, 60 * 10)
        return comments


    @classmethod
    def get_product_and_comments(cls, request, product_id):
        comments = cls.objects.select_related(
            'product', 'product__category',
             'product__category__category',).filter(product_id=product_id)
        product = comments[0].product
        django_cache.set(f'product:{request.META.get("REMOTE_ADDR")}', product)
        django_cache.set(f'comments:{product_id}:{request.META.get("REMOTE_ADDR")}', comments)
        return product, comments