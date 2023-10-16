from django.shortcuts import render
from django.views import View
from users.models import User, Profile
from .models import Header
from products.models import Category, SubCategory, SubSubCategory,Product, ProductImage
from utils.decorators import debugger
from PIL import Image
from django.db.models import F
from main.settings import cache
from django.core.cache import cache as django_cache
from django.http.response import HttpResponse


class HomeView(View):
    @debugger
    def get(self, request):
        user = cache.hgetall(f'user{request.session.get("sessionid", False)}')
        header = cache.lrange('header_home', 0, -1)
        if not header:
            header = Header.filter_with_absolute_urls(request, 'home')
        category = django_cache.get('category')
        subcategory = django_cache.get('subcategory')
        if not any([category, subcategory]):
            category, subcategory = SubCategory.all_categories_and_subcategories(request)
        products = django_cache.get(f'discounted_products{"home"}')
        if products is None:
            products = Product.filter_product_with_most_discount(request, '')
        ipaddress = request.META.get('REMOTE_ADDR')
        sub_sub_categories = django_cache.get(f'user_recent_products{ipaddress}')
        if sub_sub_categories is None:
            sub_sub_categories = SubSubCategory.all_sub_categories_with_products(request,[])
        return render(request, 'home.html', {'user': user,
                                             'category': category,
                                             'subcategory': subcategory,
                                             "sub_sub_categories": sub_sub_categories,
                                             'products': products,
                                             'header': header})
class SearchView(View):
    def get(self, request):
        pass

