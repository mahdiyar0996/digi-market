from django.shortcuts import render
from django.views import View
from users.models import User, Profile
from .models import Header
from products.models import Category, SubCategory, SubSubCategory,Product, ProductImage
from utils.decorators import debugger
from PIL import Image
from django.db.models import F, Q, Max
from main.settings import cache
from django.core.cache import cache as django_cache
from django.http.response import HttpResponse


class HomeView(View):
    @debugger
    def get(self, request):
        user = cache.hgetall(f'user{request.session.get("_auth_user_id")}')
        header = cache.lrange('header_home', 0, -1)
        if not header:
            header = Header.filter_with_absolute_urls(request, 'home')
        category = django_cache.get('category')
        subcategory = django_cache.get('subcategory')
        if not any([category, subcategory]):
            category, subcategory = SubCategory.all_categories_and_subcategories(request)
        products = django_cache.get(f'discounted_products{"home"}')
        if products is None:
            products = Product.filter_product_with_most_discount(request, category__name='home')
        ipaddress = request.META.get('REMOTE_ADDR')
        recent_views = request.COOKIES.get('by-recent-views', [])
        if isinstance(recent_views, str):
            recent_views = recent_views.split(' ')
        sub_sub_categories = django_cache.get(f'by_user_recent_views{ipaddress}')
        if sub_sub_categories is None:
            sub_sub_categories = SubSubCategory.all_sub_categories_with_products(request, recent_views)
        return render(request, 'home.html', {'category': category,
                                             'subcategory': subcategory,
                                             "sub_sub_categories": sub_sub_categories,
                                             'products': products,
                                             'header': header,
                                             'user': user})
class SearchView(View):
    @debugger
    def get(self, request):
        user = cache.hgetall(f'user{request.session.get("_auth_user_id")}')
        request.GET._mutable = True
        query_string = request.GET.get('q')
        request.GET.pop('q') if query_string else None
        if query_string:
            products = Product.objects.select_related('category').filter(
                Q(name__contains=query_string) | Q(description__contains=query_string))
            sub_subcategories = SubSubCategory.objects.filter(Q(product__name__contains=query_string) | Q(
                product__description__contains=query_string)).distinct().only('id', 'name', 'brand')
        categories = request.GET.getlist('category', False)
        request.GET.pop('category') if categories else None
        if categories and not query_string:
            products = Product.objects.select_related('category').filter(category__name__in=categories)
            sub_subcategories = SubSubCategory.objects.filter(name__in=categories
                                                              ).distinct().only('id', 'name', 'brand')
        elif categories and query_string:
            products = products.filter(category__name__in=categories)
            sub_subcategories = sub_subcategories.filter(name__in=categories)
        brands = request.GET.getlist('brand', False)
        request.GET.pop('brand') if brands else None
        if brands and not any([query_string, categories]):
            products = Product.objects.select_related('category').filter(brand__in=brands)
            sub_subcategories = SubSubCategory.objects.filter(product__brand__in=brands
                                                              ).distinct().only('id', 'name', 'brand')
        elif brands and any([query_string, categories]):
            products = products.filter(brand__in=brands)
            sub_subcategories = sub_subcategories.filter(brand__in=brands)
        min_price = int(request.GET.get('min_price', 0))
        max_price = int(request.GET.get('max_price')) if request.GET.get('max_price') else None
        if min_price or max_price and not any([brands, categories, query_string]):
            products = Product.objects.select_related('category'
                                                      ).annotate(maximum=Max('price')
                                                                 ).filter(price__gte=min_price,
                                                                          price__lte=max_price or F('maximum')
                                                                          )
            sub_subcategories = SubSubCategory.objects.annotate(Max('product__price')).filter(
                product__price__gte=min_price or 0, product__price__lte=max_price or F('max_price')
            ).distinct().only('id', 'name', 'brand')
        elif min_price or max_price and any([brands, categories, query_string]):
            products = products.annotate(maximum=Max('price')
                                         ).filter(price__gte=min_price,
                                                  price__lte=max_price or F('maximum'))
            sub_subcategories = sub_subcategories.annotate(max_price=Max('product__price')).filter(
                product__price__gte=min_price, product__price__lte=max_price or F('max_price')
            ).distinct().only('id', 'name', 'brand')

        try:
            max_price = products.aggregate(max_price=Max('price'))
            brands = {}
            for i, v in enumerate(sub_subcategories):
                for key, value in v.brand.items():
                    if value not in brands:
                        brands[key] = value
        except UnboundLocalError:
            return render(request, 'search.html', {'user': user})
        return render(request, 'search.html', {'products': products,
                                               'brands': brands,
                                               'max_price': max_price,
                                               'sub_subcategories': sub_subcategories,
                                               'user': user})
