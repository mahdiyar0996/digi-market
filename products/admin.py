from django.contrib import admin
from .models import Product, ProductImage, ProductComment, Category, SubCategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        ('مجموعه', {'fields': ('name', 'avatar' )}),
    )
    list_display = ['id', 'name', 'created_at', 'updated_at']

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        ('زیر مجموعه', {'fields': ('name', 'avatar')}),
    )
    list_display = ['id', 'name', 'created_at', 'updated_at']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fieldsets = (
        ('مشخصات محصول', {'fields': ('name', 'description', 'details', 'warranty', 'tag')}),
        ('قیمت محصول', {'fields': ('price', 'discount')}),
        (None, {'fields': ('colour', 'stock', 'avatar')}),
        ('دسترسی ها', {'fields': ('is_acitve', )}),
        (None, {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ['created_at', 'updated_at']
    list_display = ['id', 'name', 'price', 'discount', 'tag', 'stock', 'is_active', 'created_at', 'updated_at']