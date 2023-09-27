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
