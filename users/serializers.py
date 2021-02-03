from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from rest_framework import serializers
from .models import User, Identity, IDENTIFIED


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model  = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class UserSerializerRestricted(serializers.ModelSerializer):

    class Meta:
        model  = User
        fields = ['id', 'first_name', 'last_name', 'email']
        read_only_fields = ['id', 'first_name', 'last_name', 'email']