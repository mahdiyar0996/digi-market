import datetime
import pickle
from django.shortcuts import render, reverse, redirect
from django.views import View
from .models import SubCategory, Category, SubSubCategory, Product, ProductComment, ProductImage
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
from sys import getsizeof
from main.settings import cache
from django.core.cache import cache as django_cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class CategoryListView(View):
    @debugger
    def get(self, request, category):
        user = cache.hgetall(f'user{request.session.get("_auth_user_id")}')
        subcategory = django_cache.get(f'list_of_subcategories{category}')
        if subcategory is None:
            subcategory = SubCategory.filter_subcategory_with_category(request, category)
        products = django_cache.get(f'list_of_subcategories_products{category}')
        sub_sub_category = django_cache.get(f'sub_sub_categories{category}')
        if sub_sub_category is None:
            sub_sub_category = SubSubCategory.filter_categories_with_category_list(request, subcategory, category)
        if products is None:
            products = Product.filter_products_with_sub_category(request, category)
        header = cache.lrange(f'header_{category}', 0, -1)
        if len(header) <= 0:
            header = Header.filter_with_absolute_urls(request, category)
        return render(request, 'category-list.html', {'subcategory': subcategory,
                                                      'sub_sub_category': sub_sub_category,
                                                      'products': products,
                                                      'header': header,
                                                      'user': user})


class SubCategoryListView(View):
    def get(self, request, category):
        user = cache.hgetall(f'user{request.session.get("_auth_user_id")}')
        products = django_cache.get(f'products_{category}')
        max_price = django_cache.get(f'product_max_price{category}')
        sub_sub_categories = django_cache.get(f'sub_sub_categories{category}')
        if not sub_sub_categories:
            sub_sub_categories = SubSubCategory.objects.filter(category__name=category)
            django_cache.set(f'sub_sub_categories{category}', sub_sub_categories)
        if not products:
            products, max_price = Product.filter_product_with_sub_sub_category(request, category)
        if products:
            paginator = Paginator(products, 20)
            page = request.GET.get('page')
            try:
                products = paginator.page(page)
            except PageNotAnInteger:
                products = paginator.page(1)
            except EmptyPage:
                products = paginator.page(paginator.num_pages)
        else:
            paginator = None
        return render(request, 'subcategory-list.html', {'products': products,
                                                         'max_price': max_price,
                                                         'user': user,
                                                         'sub_sub_categories': sub_sub_categories,
                                                         'paginator': paginator})



class SubSubCategoryList(View):
    def get(self, request, category):
        user = cache.hgetall(f'user{request.session.get("_auth_user_id")}')
        page = request.GET.get('page', 1)
        products = django_cache.get(f'products_{category}')
        max_price = django_cache.get(f'product_max_price{category}')
        if products is None:
            products, max_price = Product.filter_products_and_get_sub_sub_categories(request, category, page)
        paginator = Paginator(products, 20)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        sub_sub_category = django_cache.get(category)
        if sub_sub_category is None:
            sub_sub_category = SubSubCategory.objects.only('name', 'details', 'brand').get(name=category)
            django_cache.set(category, sub_sub_category)
        print(max_price)
        return render(request, 'sub-subcategory-list.html', {'products': products,
                                                             'paginator': paginator,
                                                             'category': sub_sub_category,
                                                             'max_price': max_price,
                                                             "user": user})


class ProductDetailsView(View):
    def get(self, request, category, product_id,):
        form = ProductCommentForm
        user = cache.hgetall(f'user{request.session.get("_auth_user_id", False)}')
        product = django_cache.get(f'product:{product_id}')
        product_images = django_cache.get(f'images:{product_id}')
        if not any([product, product_images]):
            product, product_images = ProductImage.get_product_and_images(request, product_id)
        product_comments = django_cache.get(f'comments:{product_id}', False)
        if not product_comments and not cache.keys(f'*comments:{product_id}'):
            product_comments = ProductComment.is_active_comments(product_id)
        try:
            product_details = product.details.items()
        except AttributeError:
            product_details = None
        if len(product_comments) > 0:
            average = get_average(product_comments)
            comment_counts = get_count(product_comments)
        else:
            average = 0
            comment_counts = 0
            product_comments = None
        try:
            is_in_basket = UserBasket.get_basket_product_counts(user['username'], product_id)
        except (UserBasket.DoesNotExist, KeyError):
            is_in_basket = None
        response = render(request, 'product-details.html', {'product': product, 'product_images': product_images,
                                                        'product_details': product_details,
                                                        'product_comments': product_comments,
                                                        'comment_counts': comment_counts, 'form': form,
                                                        'average': average,
                                                        'is_in_basket': is_in_basket,
                                                        'user': user})
        recent_view = request.COOKIES.get('by-recent-views', False)
        if recent_view:
            if str(product.category.id) not in recent_view:
                response.set_cookie('by-recent-views', recent_view + f' {product.category.id}')
                if len(request.COOKIES.get('by-recent-views')) > 40:
                    recent_view = request.COOKIES.get('by-recent-views').split(' ')
                    del recent_view[0]
        else:
            response.set_cookie('by-recent-views', str(product.category.id))
        return response

    def post(self, request, category, product_id):
        try:
            if request.POST.get('delete-from-basket', False):
                UserBasket.objects.filter(profile=request.user.profile, product__id=product_id).delete()

        except UserBasket.DoesNotExist:
            pass
        if request.POST.get('add-to-basket', False):
            if request.user.is_authenticated:
                try:
                    product = Product.objects.get(id=product_id)
                    UserBasket.objects.create(profile=request.user.profile, product=product)
                except IntegrityError:
                    pass
            else:
                messages.error(request, 'ابتدا وارد حساب خود شوید', 'add-to-basket')
                print('dsfsd')
        if request.POST.get('add-more', False):
            try:
                add_more_to_basket = UserBasket.objects.get(profile=request.user.profile, product__id=product_id)
                add_more_to_basket.count += 1
                add_more_to_basket.save()
            except (UserBasket.DoesNotExist, IntegrityError):
                pass

        if request.POST.get('comment'):
            form = ProductCommentForm(request.POST)
            if form.is_valid():
                product_name = Product.objects.get(id__exact=product_id, category__name__exact=category)
                cp = form.cleaned_data
                try:
                    ProductComment.objects.create(product=product_name, user=request.user,
                                                            comment=cp['comment'], rating=cp['rating'])
                    messages.success(request, 'دیدگاه شما ارسال شد و بعد از تایید شدن قرار گرفته میشود', 'comment')
                except ValueError:
                    messages.error(request, 'برای ارسال نظر باید وارد حساب خود شوید', 'comment')
                return redirect('product-details', category, product_id)
            return HttpResponseBadRequest
        return redirect('product-details', category, product_id)
