from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import HomeView, SearchView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search/', SearchView.as_view(), name='search')
]