from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]