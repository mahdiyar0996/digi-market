from django.shortcuts import render
from django.views import View
from .models import SubCategory, Category, Product, ProductComment, ProductImage
from core.models import Header
from utils.decorators import debugger

class CategoryListView(View):
    @debugger
    def get(self, request, category):
        subcategory = SubCategory.objects.filter(category__name=category)
        header = Header.objects.filter(name=category)
        return render(request, 'category-list.html', {'subcategory': subcategory, 'header': header})


class ProductListView(View):
    def get(self, request, category):
        products = Product.objects.filter(category__name=category)
        return render(request, 'product-list.html', {'products': products})

class ProductDetailsView(View):
    @debugger
    def get(self, request, product, category):


        product = Product.objects.select_related('category').get(name=product, category__name=category)
        product_images = ProductImage.objects.filter(product=product)
        # similar_products = Product.objects.filter(tag__exact=product.tag)
        # print(product.productimage.count())
        product_details = product.details.items()
        return render(request, 'product-details.html', {'product': product, 'product_images': product_images,
                                                        'product_details': product_details})