from django.shortcuts import render
from django.views import View
from users.models import User, Profile
from .models import Header
from utils.decorators import debugger
from PIL import Image
class HomeView(View):
    @debugger
    def get(self, request):
        try:
            profile = Profile.objects.select_related('user').get(user=request.user)
        except Profile.DoesNotExist:
            return render(request, 'home.html')
        user = profile.user
        header = Header.objects.all()
        return render(request, 'home.html', {'user': user, 'profile': profile, 'header': header})
