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
        query_string = request.GET.get('q')
        products = Product.objects.select_related('category').filter(Q(name__contains=query_string) | Q(description__contains=query_string))
        max_price = Product.objects.filter(Q(name__contains=query_string) | Q(description__contains=query_string)).aggregate(max_price=Max('price'))
        sub_subcategories = SubSubCategory.objects.filter(Q(product__name__contains=query_string) | Q(product__description__contains=query_string)).distinct().only('id', 'name', 'brand')
        brands = {}
        for i, v in enumerate(sub_subcategories):
            for key, value in v.brand.items():
                if value not in brands:
                    brands[key] = value
        return render(request, 'search.html', {'products': products,
                                               'brands': brands,
                                               'max_price': max_price,
                                               'sub_subcategories': sub_subcategories,
                                               'user': user})
