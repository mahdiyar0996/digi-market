from users.models import User, Profile
from rest_framework.views import APIView, Response
from .serializers import UserSerializer, ProfileSerializer
from django.db.models import Q, F, Prefetch
from utils.decorators import debugger
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND
from rest_framework import mixins, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from .backends import CustomBasicAuthentication
from rest_framework.decorators import permission_classes
from .permissions import FullPermission
from rest_framework.reverse import reverse
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


class ApiUserListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    queryset = User.objects.select_related('profile').only('username', 'email', 'phone_number',
                                                           'password', 'credits', 'address',
                                                           'is_superuser', 'is_staff',
                                                           'is_active', "profile").all()
    serializer_class = UserSerializer
    lookup_field = 'pk'

    @method_decorator(cache_page(60 * 2, key_prefix='users-api'))
    def get(self, request, *args, **kwargs):
        s = request.headers.get('Authorization')
        print(type(s))
        return super().get(request, *args, **kwargs)


class ApiUserDetailsView(generics.RetrieveAPIView,
                         generics.DestroyAPIView,
                         generics.UpdateAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [FullPermission]
    serializer_class = UserSerializer

    @debugger
    @method_decorator(cache_page(60 * 15, key_prefix='users-details-api'))
    @method_decorator(vary_on_headers("Authorization", ))
    def get(self, request, *args, **kwargs):
        if self.get_object() is None:
            return Response(status=HTTP_404_NOT_FOUND)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        try:
            query = User.objects.select_related('profile').only('username', 'email', 'phone_number',
                                                                'password', 'credits', 'address',
                                                                'is_superuser', 'is_staff', 'is_active',
                                                                'profile__avatar', 'profile__first_name',
                                                                'profile__last_name').get(pk=self.kwargs.get('pk'))
        except User.DoesNotExist:
            query = None
        return query

    def get_object(self):
        queryset = self.get_queryset()
        self.check_object_permissions(self.request, queryset)
        return queryset

    # def filter_queryset(self, queryset):
    #     filter_backends = [CategoryFilter]
    #
    #     if 'geo_route' in self.request.query_params:
    #         filter_backends = [GeoRouteFilter, CategoryFilter]
    #     elif 'geo_point' in self.request.query_params:
    #         filter_backends = [GeoPointFilter, CategoryFilter]
    #
    #     for backend in list(filter_backends):
    #         queryset = backend().filter_queryset(self.request, queryset, view=self)
    #
    #     return queryset
    #     def get_serializer_class(self):
    #         if self.request.user.is_staff:
    #             return FullAccountSerializer
    #         return BasicAccountSerializer