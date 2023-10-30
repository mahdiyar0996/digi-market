from django.db.models.signals import post_save, post_delete, pre_delete, pre_save
from django.dispatch import receiver, Signal
from .models import Product
from main.settings import cache


