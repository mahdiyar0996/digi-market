from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin, GroupAdmin, Group
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import User,Profile
from .forms import RegisterForm


# @admin.register(AdminGroup)
# class GroupAdmin(GroupAdmin):
#     list_display = ['name',]

class ProfileAdmin(admin.StackedInline):
    model = Profile
    readonly_fields = ['updated_at']
    fields = ['avatar', 'first_name', 'last_name', 'age', 'job', 'updated_at']
@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        ('User Info', {'fields': ('username', 'email', 'phone_number', 'password', 'credits')}),
        ('Personal Info', {"fields": ('city', 'address')}),
        ("Permissions", {'fields': ('is_superuser', 'is_staff', 'is_active', 'groups', 'ipaddress')}),
        ('DATE AND TIME', {'fields': ('created_at', 'updated_at', "last_login", 'last_password_reset')})
    )
    readonly_fields = ['updated_at', 'created_at', 'last_login', 'last_password_reset']
    list_display = ['id', 'username', 'email', 'phone_number', 'is_active', 'is_staff', 'is_superuser','created_at', 'updated_at', 'last_login']
    list_display_links = ['id', 'username', 'email', 'phone_number']
    list_per_page = 100
    list_filter = ['is_superuser', 'is_staff', 'is_active']
    search_fields = ['id', 'username', 'email', 'phone_number']
    inlines = [ProfileAdmin]




admin.site.index_title = "my site"
admin.site.site_header = "my header"
admin.site.site_title = "hello world"





