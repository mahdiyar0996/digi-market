from django.shortcuts import render
from django.views import View
from .models import Header
from products.models import SubCategory, SubSubCategory, Product
from utils.decorators import debugger
from django.db.models import F, Q, Max
from main.settings import cache
from django.core.cache import cache as django_cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
            products = Product.filter_product_with_most_discount(request,discount=0 ,category__name='home')
        ipaddress = request.META.get('REMOTE_ADDR')

        recent_views = request.COOKIES.get('by-recent-views', [])
        if isinstance(recent_views, str):
            recent_views = recent_views.split(' ')

        sub_sub_categories = django_cache.get(f'by_user_recent_views{ipaddress}')

        if sub_sub_categories is None:
            sub_sub_categories = SubSubCategory.all_sub_categories_with_products(request, recent_views)

        context = {
            'category': category,
            'subcategory': subcategory,
            'sub_sub_categories': sub_sub_categories,
            'products': products,
            'header': header,
            'user': user
        }

        return render(request, 'home.html', context)


class SearchView(View):
    @debugger
    def get(self, request):
        user = cache.hgetall(f'user{request.session.get("_auth_user_id")}')
        request.GET._mutable = True

        products = Product.objects.select_related('category').only('category__name', 'name',
                                                                   'brand', 'price',
                                                                   'discount', 'is_active',
                                                                   'stock', 'avatar')
        sub_subcategories = SubSubCategory.objects.only('id', 'name', 'brand')

        query_string = request.GET.get('q')

        categories = request.GET.getlist('category', False)

        brands = request.GET.getlist('brand', False)

        min_price = int(request.GET.get('min_price', 0))
        max_price = int(request.GET.get('max_price')) if request.GET.get('max_price') else None

        is_active = request.GET.get('is_active', False)
        if query_string:
            products = products.filter(
                Q(name__contains=query_string) | Q(description__contains=query_string)
            )
            sub_subcategories = sub_subcategories.filter(
                Q(product__name__contains=query_string) | Q(product__description__contains=query_string)
            ).distinct()

        if categories:
            products = products.filter(category__name__in=categories)
            sub_subcategories = sub_subcategories.filter(name__in=categories).distinct()

        if brands:
            products = products.filter(brand__in=brands)
            sub_subcategories = sub_subcategories.filter(product__brand__in=brands).distinct()

        if min_price or max_price:
            products = products.annotate(maximum=Max('price')).filter(
                price__gte=min_price,
                price__lte=max_price or F('maximum')
            )
            sub_subcategories = sub_subcategories.annotate(max_price=Max('product__price')).filter(
                product__price__gte=min_price or 0,
                product__price__lte=max_price or F('max_price')
            ).distinct()

        if is_active:
            products = products.filter(is_active=True)
            sub_subcategories = sub_subcategories.filter(product__is_active=True).distinct()

        try:
            max_price = products.aggregate(max_price=Max('price'))
            brands = {}
            for subsubcategory in sub_subcategories:
                for key, value in subsubcategory.brand.items():
                    if value not in brands:
                        brands[key] = value
        except UnboundLocalError:
            return render(request, 'search.html', {'user': user})

        page = request.GET.get('page', 1)
        paginator = Paginator(products, 20)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        return render(request, 'search.html', {
            'products': products,
            'paginator': paginator,
            'brands': brands,
            'max_price': max_price,
            'sub_subcategories': sub_subcategories,
            'user': user
        })
