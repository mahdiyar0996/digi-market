import datetime

from django.shortcuts import render, reverse, redirect
from django.views import View
from .models import SubCategory, Category, Product, ProductComment, ProductImage
from users.models import UserBasket
from core.models import Header
from utils.decorators import debugger
from django.db.models import Count, Avg, Q
from django.core.cache import cache
from .forms import ProductCommentForm
from django.contrib import messages
from django.http.response import HttpResponseBadRequest
from utils.tools import get_average, get_avg, get_count
from django.core.exceptions import BadRequest
from django.db import IntegrityError
class CategoryListView(View):
    @debugger
    def get(self, request, category):
        subcategory = SubCategory.objects.filter(category__name=category)
        header = Header.objects.filter(name=category)
        return render(request, 'category-list.html', {'subcategory': subcategory, 'header': header})


class ProductListView(View):
    @debugger
    def get(self, request, category):
        products = Product.objects.select_related('category').filter(category__name=category)
        print(products)
        products_comments_average = ProductComment.objects.select_related('product').filter(is_active=True, product__in=products).annotate(average=Avg('rating'))
        return render(request, 'product-list.html', {'products': products, 'products_comments_average': products_comments_average})


class ProductDetailsView(View):
    @debugger
    def get(self, request, category, product_id,):
        form = ProductCommentForm
        product_images = ProductImage.objects.select_related('product', 'product__category',
                                                                 'product__category__category',
                                                             ).filter(product__id=product_id)
        product_comments = ProductComment.is_active_comments(product_id)
        try:
            product = product_images[0].product
            try:
                product_details = product.details.items()
            except AttributeError:
                product_details = None
            if len(product_comments) > 0:
                average = get_average(product_comments)
                comment_counts = len(product_comments)
            else:
                average = 0
                comment_counts = 0
        except (IndexError, TypeError):
            raise BadRequest

        try:
            if request.GET.get('delete-from-basket', False):
                UserBasket.objects.filter(user=request.user, product=product).delete()

        except (UserBasket.DoesNotExist):
            pass
        if request.GET.get('add-to-basket', False):
            try:
                add_to_basket = UserBasket.objects.create(user=request.user, product=product)
                is_in_basket = add_to_basket
            except IntegrityError:
                is_in_basket = UserBasket.objects.get(user=request.user, product=product)
        if request.GET.get('add-more', False):
            try:
                add_more_to_basket = UserBasket.objects.get(user=request.user, product=product)
                add_more_to_basket.count += 1
                add_more_to_basket.save()
                is_in_basket = add_more_to_basket
            except (UserBasket.DoesNotExist, IntegrityError):
                pass

        else:
            try:
                is_in_basket = UserBasket.objects.get(user=request.user, product=product)
            except UserBasket.DoesNotExist:
                is_in_basket = None
        return render(request, 'product-details.html', {'product': product, 'product_images': product_images,
                                                        'product_details': product_details, 'product_comments': product_comments,
                                                        'comment_counts': comment_counts, 'form': form,
                                                        'average': average,
                                                        'is_in_basket': is_in_basket})
    @debugger
    def post(self, request, category, product_id):
        form = ProductCommentForm(request.POST)
        if form.is_valid():
            product_name = Product.objects.get(id__exact=product_id, category__name__exact=category)
            cp = form.cleaned_data
            ProductComment.objects.create(product=product_name, user=request.user,
                                                    comment=cp['comment'], rating=cp['rating'])

            messages.success(request, 'دیدگاه شما ارسال شد و بعد از تایید شدن قرار گرفته میشود', 'success')
            return redirect('product-details', category, product_id)
        print(form.errors)
        return HttpResponseBadRequest
