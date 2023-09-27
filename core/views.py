from django.shortcuts import render
from django.views import View
from users.models import User, Profile
from .models import Header
from products.models import Category, SubCategory
from utils.decorators import debugger
from PIL import Image


class HomeView(View):
    @debugger
    def get(self, request):
        header = Header.objects.all()
        subcategory = SubCategory.objects.all()[:12]
        category = Category.objects.all()
        try:
            profile = Profile.objects.select_related('user').get(user=request.user)
        except (Profile.DoesNotExist, TypeError):
            return render(request, 'home.html', {'category': category, 'subcategory': subcategory})
        user = profile.user
        return render(request, 'home.html', {'user': user, 'profile': profile,
                                             'category': category,
                                             'subcategory': subcategory,
                                             'header': header})


