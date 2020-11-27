from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

import users.validators as custom_validator
from ..models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'code', 'avatar', 'groups', 'date_joined']


class SignupSerializer(serializers.Serializer):
    username = serializers.EmailField(
        label=_('username'),
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    first_name = serializers.CharField(label=_('firstname'))
    last_name = serializers.CharField(label=_('lastname'))

    # code = serializers.CharField(label=_('code'))
    # identifier_image = serializers.ImageField(_('identifier'))

    def create(self, validated_data):
        """ Create and return a new `user` instance, given the validated data. """
        return User.objects.create_user(email=validated_data.pop('username'),
                                        password=validated_data.pop('password'), **validated_data)

    # def update(self, instance, validated_data):
    #     """ Update and return an existing `user` instance, given the validated data. """
    #     instance.username = validated_data.get('username')
    #     instance.first_name = validated_data.get('first_name')
    #     instance.last_name = validated_data.get('last_name')
    #     instance.code = validated_data.get('code')
    #     instance.identifier_image = validated_data.get('identifier_image')
    #     instance.save()
    #     return instance

    def validate(self, attrs):
        if User.objects.filter(email=attrs.get('username')):
            raise serializers.ValidationError("email address has been taken befor")
        return attrs

    def validate_username(self, email):
        if custom_validator.validate_email(email):
            return email
        raise serializers.ValidationError('not valid username')

    def validate_password(self, password):
        if custom_validator.validate_password(password):
            return password
        raise serializers.ValidationError('not valid password')

    def validate_first_name(self, firstname):
        if custom_validator.validate_firstname(firstname):
            return firstname
        raise serializers.ValidationError('not valid firstname')

    def validate_last_name(self, lastname):
        if custom_validator.validate_lastname(lastname):
            return lastname
        raise serializers.ValidationError('not valid lastname')

    def validate_code(self, code):
        if custom_validator.validate_identifier_code(code):
            return code
        raise serializers.ValidationError('not valid identifier code')

    def validate_identifier_image(self, image):
        if custom_validator.validate_identifier_image(image):
            return image
        raise serializers.ValidationError('not valid identifier image')
