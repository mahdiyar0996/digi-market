from django.contrib import admin
from .models import Header

@admin.register(Header)
class HeaderAdmin(admin.ModelAdmin):
    field = '__all__'