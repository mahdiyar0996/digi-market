from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer, Serializer
from rest_framework import serializers
from users.models import User, Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # pass
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        cls.token_class
        return token


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ['avatar', 'first_name', 'last_name', 'age', 'job']


class UserSerializer(ModelSerializer):
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'phone_number',
                  'password', 'credits', 'address', 'is_superuser', 'is_staff', 'is_active', 'profile')
        extra_kwargs = {
            'url': {'view_name': 'user-detail-api'}
        }