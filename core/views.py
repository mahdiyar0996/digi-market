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
        subcategory = SubCategory.objects.select_related('category').all()
        category = [category.foreign for category in subcategory]
        print(category)
        print(header)
        try:
            profile = Profile.objects.select_related('user').get(user=request.user)
        except (Profile.DoesNotExist, TypeError):
            return render(request, 'home.html')
        user = profile.user
        return render(request, 'home.html', {'user': user, 'profile': profile, 'header': header})
