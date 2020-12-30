from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model  = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class UserSerializerRestricted(serializers.ModelSerializer):

    class Meta:
        model  = User
        fields = ['id', 'first_name', 'last_name', 'email']
        extra_kwargs = {
            'id': {'read_only': True},
            'first_name': {'read_only': True},
            'last_name': {'read_only': True}
        }
