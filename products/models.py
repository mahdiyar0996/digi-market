from django.db import models
from .managers import ProductManager
from django.db.models import Sum, Count, F


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
    category = models.ForeignKey(Category,verbose_name='مجموعه', related_name='%(class)s', on_delete=models.DO_NOTHING)
    avatar = models.ImageField("آواتار", upload_to='products/subcategory/avatar/')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "sub_categories"
        verbose_name = 'sub_category'
        verbose_name_plural = 'sub_categories'


class Product(BaseAbstract):
    category = models.ForeignKey(SubCategory, verbose_name='مجموعه', related_name='%(class)s', on_delete=models.DO_NOTHING)
    description = models.TextField("درباره کالا", max_length=1000, blank=True,)
    details = models.JSONField("جزییات", blank=True, null=True)
    warranty = models.CharField("گارانتی", max_length=255, blank=True)
    tag = models.CharField(max_length=55, blank=True, db_index=True)
    price = models.BigIntegerField("قیمت", blank=True, null=True)
    discount = models.CharField('تخفیف', max_length=55, blank=True)
    is_active = models.BooleanField('وضعیت', default=True, db_index=True)
    colour = models.CharField("رنگ", max_length=55, blank=True,)
    stock = models.BigIntegerField("تعداد کالا", blank=True, null=True)
    avatar = models.ImageField('آواتار', blank=True, null=True, upload_to='products/avatar/')
    objects = ProductManager

    class Meta:
        db_table = 'products'
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ['created_at', 'stock', 'price']

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product,verbose_name='کالا', related_name='%(class)s', on_delete=models.CASCADE, db_index=True)
    images = models.ImageField('عکس ها', upload_to='products/images/', blank=True)

    class Meta:
        db_table = 'products_images'
        verbose_name = 'product_image'
        verbose_name_plural = 'products_images'
    def __str__(self):
        return self.product.name


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
        return ProductComment.objects.select_related('user').filter(product__id=product_id, is_active=True)