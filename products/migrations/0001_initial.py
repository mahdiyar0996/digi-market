# Generated by Django 4.2 on 2023-09-27 08:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='نام')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ انتشار')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین اپدیت')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='نام')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ انتشار')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین اپدیت')),
                ('description', models.TextField(blank=True, max_length=1000, verbose_name='درباره کالا')),
                ('details', models.JSONField(blank=True, null=True, verbose_name='جزییات')),
                ('warranty', models.CharField(blank=True, max_length=255, verbose_name='گارانتی')),
                ('tag', models.CharField(blank=True, db_index=True, max_length=55)),
                ('price', models.BigIntegerField(blank=True, null=True, verbose_name='قیمت')),
                ('discount', models.CharField(blank=True, max_length=55, verbose_name='تخفیف')),
                ('colour', models.CharField(blank=True, max_length=55, verbose_name='رنگ')),
                ('stock', models.BigIntegerField(blank=True, null=True, verbose_name='تعداد کالا')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='products/avatar/', verbose_name='آواتار')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'db_table': 'products',
                'ordering': ['created_at', 'stock', 'price'],
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='نام')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ انتشار')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین اپدیت')),
                ('foreign', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s', to='products.category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(blank=True, upload_to='products/images/', verbose_name='عکس ها')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s', to='products.product')),
            ],
            options={
                'verbose_name': 'product-image',
                'verbose_name_plural': 'products-images',
                'db_table': 'product-images',
            },
        ),
        migrations.CreateModel(
            name='ProductComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ انتشار')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین اپدیت')),
                ('rating', models.IntegerField(blank=True, db_index=True, default=10, null=True, verbose_name='امتیاز')),
                ('comment', models.TextField(verbose_name='دیدگاه')),
                ('is_active', models.BooleanField(db_index=True, default=False, verbose_name='وضعیت')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s', to='products.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'product-comment',
                'verbose_name_plural': 'products-comments',
                'db_table': 'products-comments',
                'ordering': ['rating', 'updated_at', 'created_at'],
            },
        ),
    ]
