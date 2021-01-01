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
            'last_name': {'read_only': True},
            'email': {'read_only': True}
        }

    #def validate(self, attrs):
        #print("Fucking HERE")
        #return attrs
    # hello. if you see this, validate and validate_identity is not actually working.
    # I actually tried to fix it and identify the users that i pass but validate and
    # validate_identity just don't work actually.