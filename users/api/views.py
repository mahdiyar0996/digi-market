from django.urls import path, include
from users.models import User, Profile
from rest_framework.views import APIView, Response
from .serializers import UserSerializer, ProfileSerializer
from django.db.models import Q, F, Prefetch
from utils.decorators import debugger
from rest_framework.status import HTTP_200_OK
from rest_framework.renderers import JSONRenderer
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND
from rest_framework import mixins, generics

class ApiUserView(APIView):
    @debugger
    def get(self, request, format=None):
        _id = request.GET.get('id', False)
        username = request.GET.get('username', False)
        email = request.GET.get('email', False)
        phone_number = request.GET.get('phone_number', False)
        if any([username, email, phone_number]):
            try:
                user = User.objects.select_related('profile').filter(Q(id__exact=_id) |
                                                                     Q(username__exact=username) |
                                                                     Q(email__exact=email) |
                                                                     Q(phone_number__exact=phone_number))
            except User.DoesNotExist:
                return Response(status=HTTP_404_NOT_FOUND)
        else:
            user = User.objects.select_related('profile').all()
        serializer = UserSerializer(user, many=True, context={'request': request})
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            try:
                serializer.profile.save()
            except AttributeError:
                pass
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            user = User.objects.select_related('profile').get(Q(id=request.data.get('id')) |
                                                          Q(username=request.data.get('username')))
        except User.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            try:
                serializer.profile.save()
            except AttributeError:
                pass
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.data, status=HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            user = User.objects.get(Q(id=request.data.get('id')) |
                                    Q(username=request.data.get('username')) |
                                    Q(email=request.data.get('email')))
        except User.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=HTTP_200_OK)


class ApiUserDetailsView(generics.RetrieveAPIView):
    queryset = User.objects.select_related('profile').only('username', 'email', 'phone_number',
                                                           'password', 'credits', 'address',
                                                           'is_superuser', 'is_staff', 'is_active',
                                                           'profile__avatar', 'profile__first_name',
                                                           'profile__last_name').all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)