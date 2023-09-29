from django.shortcuts import render, reverse, redirect
from django.views import View
from .models import SubCategory, Category, Product, ProductComment, ProductImage
from core.models import Header
from utils.decorators import debugger
from django.db.models import Count
from django.core.cache import cache
from .forms import ProductCommentForm
from django.contrib import messages
from django.http.response import HttpResponseBadRequest
from utils.tools import get_average
class CategoryListView(View):
    @debugger
    def get(self, request, category):
        subcategory = SubCategory.objects.filter(category__name=category)
        header = Header.objects.filter(name=category)
        return render(request, 'category-list.html', {'subcategory': subcategory, 'header': header})


class ProductListView(View):
    def get(self, request, category):
        products = Product.objects.filter(category__name=category)
        print(products)
        return render(request, 'product-list.html', {'products': products})


class ProductDetailsView(View):
    @debugger
    def get(self, request, category, product_id,):
        product_comments = ProductComment.objects.select_related('product', 'product__category',
                                                                 'product__category__category',
                                                                 'user').filter(product__id=product_id)

        product = product_comments[0].product
        product_details = product.details.items()
        average = get_average(product_comments)
        comment_counts = len(product_comments)
        product_images = ProductImage.objects.filter(product=product)
        form = ProductCommentForm
        return render(request, 'product-details.html', {'product': product, 'product_images': product_images,
                                                        'product_details': product_details, 'product_comments': product_comments,
                                                        'comment_counts': comment_counts, 'form': form,
                                                        'average': average})
    @debugger
    def post(self, request, category, product_id):
        form = ProductCommentForm(request.POST)
        if form.is_valid():
            product_name = Product.objects.get(id__exact=product_id, category__name__exact=category)
            cp = form.cleaned_data
            comment = ProductComment.objects.create(product=product_name, user=request.user,
                                                    comment=cp['comment'], rating=cp['rating'])

            messages.success(request, 'دیدگاه شما ارسال شد و بعد از تایید شدن قرار گرفته میشود', 'success')
            return redirect('product-details', category, product_id)

        return HttpResponseBadRequest
        # return redirect('product-details', category, product_id)