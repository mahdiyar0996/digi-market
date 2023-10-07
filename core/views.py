from django.shortcuts import render
from django.views import View
from users.models import User, Profile
from .models import Header
from products.models import Category, SubCategory, Product, ProductImage
from utils.decorators import debugger
from PIL import Image
from django.db.models import F
from main.settings import cache
from django.core.cache import cache as django_cache


class HomeView(View):
    @debugger
    def get(self, request):
        user = cache.hgetall(f'user{request.session.get("sessionid", False)}')
        header = cache.lrange('header_home', 0, -1)
        if not header:
            header = Header.filter_with_absolute_urls(request, 'home')
        category = django_cache.get('category')
        subcategory = django_cache.get('subcategory')
        if not any([subcategory is not None, category is not None]):
            subcategory, category = SubCategory.all_subcategory_and_category(request)
        return render(request, 'home.html', {'user': user,
                                             'category': category,
                                             'subcategory': subcategory,
                                             'header': header})


