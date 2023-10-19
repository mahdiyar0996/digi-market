from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer, Serializer
from rest_framework import serializers
from users.models import User, Profile





class ProfileSerializer(ModelSerializer):

    class Meta:
        model = Profile
        fields = ['avatar', 'first_name', 'last_name']


class UserSerializer(ModelSerializer):
    profile = ProfileSerializer(required=False)
    class Meta:
        model = User
        # field = ('__all__')
        fields = ('id', 'username', 'email', 'phone_number',
                  'password', 'credits', 'address', 'is_superuser', 'is_staff', 'is_active' ,'profile')
