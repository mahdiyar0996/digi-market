from django.contrib import admin
from .models import Product, ProductImage, ProductComment, Category, SubCategory
import json


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        ('مجموعه', {'fields': ('name', 'avatar' )}),
    )
    list_display = ['id', 'name', 'created_at', 'updated_at']

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        ('زیر مجموعه', {'fields': ('category', 'name', 'avatar')}),
    )
    list_display = ['id', 'name', 'created_at', 'updated_at']


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
    fields = ['images', ]
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fieldsets = (
        ('مشخصات محصول', {'fields': ('category', 'name', 'description', 'details', 'warranty', 'tag')}),
        ('قیمت محصول', {'fields': ('price', 'discount')}),
        (None, {'fields': ('colour', 'stock', 'avatar')}),
        ('دسترسی ها', {'fields': ('is_active', )}),
        (None, {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ['created_at', 'updated_at']
    list_display = ['id', 'name', 'price', 'discount', 'tag', 'stock', 'is_active', 'created_at', 'updated_at']
    inlines = [ProductImageAdmin,]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        try:
            ProductImage.objects.get(product=obj)
        except (ProductImage.DoesNotExist, ValueError):
            ProductImage.objects.create(product=obj, images=obj.avatar)
            pass

@admin.register(ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'updated_at']
    fields = ['product', 'user', 'rating', 'comment', 'is_active', 'created_at', 'updated_at']
    list_display = ['product', 'user', 'is_active', 'created_at', 'updated_at']