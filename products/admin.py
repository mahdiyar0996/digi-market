from django.contrib import admin
from .models import Product, ProductImage, ProductComment, Category, SubCategory, SubSubCategory
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


@admin.register(SubSubCategory)
class SubSubCategoryAdmin(admin.ModelAdmin):
    fields = ['category', 'name','avatar', 'brand', 'details']


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
    fields = ['images', ]
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fieldsets = (
        ('مشخصات محصول', {'fields': ('category', 'name', 'brand', 'description', 'details', 'warranty')}),
        ('قیمت محصول', {'fields': ('price', 'discount')}),
        (None, {'fields': ('colour', 'stock', 'avatar')}),
        ('دسترسی ها', {'fields': ('is_active', )}),
        (None, {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ['created_at', 'updated_at']
    list_display = ['id', 'name', 'price', 'discount', 'stock', 'is_active', 'created_at', 'updated_at']
    inlines = [ProductImageAdmin]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        try:
            ProductImage.objects.get(product=obj)
        except (ProductImage.DoesNotExist,ProductImage.MultipleObjectsReturned, ValueError):
            ProductImage.objects.create(product=obj, images=obj.avatar)
            pass


@admin.register(ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'updated_at']
    fields = ['product', 'user', 'rating', 'comment', 'is_active', 'created_at', 'updated_at']
    list_display = ['product', 'user', 'is_active', 'created_at', 'updated_at']


{
    "امکانات ظاهری":"دسته بی سیم",
    "تعداد دسته":"دو عدد",
    "فناوری‌های ارتباطی":"بلوتوث، Wi-Fi، پورت HDMI، پورت USB، پورت Lan"
}