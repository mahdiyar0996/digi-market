from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import CategoryListView

urlpatterns = [
    path('category/<str:category>/', CategoryListView.as_view(), name='subcategory')
]