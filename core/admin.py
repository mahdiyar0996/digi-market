from django.contrib import admin
from  django.contrib.auth.models import Group
from .models import Header


admin.site.unregister(Group)
@admin.register(Header)
class HeaderAdmin(admin.ModelAdmin):
    field = '__all__'