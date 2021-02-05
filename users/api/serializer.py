import datetime
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.exceptions import AuthenticationFailed

import users.validators as validator
from ..models import User, Identity, REQUESTED


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'code', 'avatar', 'date_joined']


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=_('email'),
    )
    password = serializers.CharField(
        label=_("Password"),
        min_length=6,
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    first_name = serializers.CharField(label=_('firstname'))
    last_name = serializers.CharField(label=_('lastname'))

    def create(self, validated_data):
        """ Create and return a new `user` instance, given the validated data. """
        return User.objects.create_user(email=validated_data.pop('email'),
                                        password=validated_data.pop('password'), **validated_data)

    def update(self, instance, validated_data):
        """ Update and return an existing `user` instance, given the validated data. """
        instance.email = validated_data.get('email')
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.code = validated_data.get('code')
        instance.identifier_image = validated_data.get('identifier_image')
        instance.save()
        return instance

    def validate(self, attrs):
        if User.objects.filter(email=attrs.get('email')):
            raise serializers.ValidationError("email address has been taken befor")
        return attrs

    def validate_email(self, email):
        if validator.validate_email(email):
            return email
        raise serializers.ValidationError('not valid email')

    def validate_first_name(self, firstname):
        if validator.validate_firstname(firstname):
            return firstname
        raise serializers.ValidationError('not valid firstname')

    def validate_last_name(self, lastname):
        if validator.validate_lastname(lastname):
            return lastname
        raise serializers.ValidationError('not valid lastname')

    def validate_code(self, code):
        if validator.validate_identifier_code(code):
            return code
        raise serializers.ValidationError('not valid identifier code')

    def validate_identifier_image(self, image):
        if validator.validate_identifier_image(image):
            return image
        raise serializers.ValidationError('not valid identifier image')


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=_('email'),
        write_only=True,
        required=True,
    )

    def save(self, **kwargs):
        request = self.context['request']
        email = self.validated_data['email']
        user = User.objects.get(email=email)

        uib64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)

        relative_link = reverse('users:reset_password_confirm_credential',
                                request=request, kwargs={'uib64': uib64, 'token': token})

        email_title = 'change password link for TickSy'
        email_body = 'hello\nuse this link below to reset your password\n{link}'.format(link=relative_link)

        send_mail(
            email_title,  ## title
            email_body,  ## body
            'no-reply-khu@margay.ir',  ## from
            [email, ],  ## to
        )

    def validate(self, attrs):
        if not validator.validate_email(attrs['email']):
            raise serializers.ValidationError('not valid email')
        if not User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError('no user with this email!')
        return attrs


class ResetPasswordNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        label=_('password'),
        required=True,
        min_length=6,
        write_only=True,
        style={'input_type': 'password'},
        trim_whitespace=False,
    )
    uib64 = serializers.CharField(
        label='id',
        required=True,
        min_length=1,
        write_only=True,
    )
    token = serializers.CharField(
        label='token',
        required=True,
        min_length=1,
        write_only=True,
    )

    def validate(self, attrs):
        password = attrs.get('password')
        token = attrs.get('token')
        uib64 = attrs.get('uib64')

        user_id = smart_str(urlsafe_base64_decode(uib64))
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed('کاربر با این مشخصات موجود نیست', 401)

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise AuthenticationFailed('لینک تغییر رمز نامعتبر', 401)

        user.set_password(password)
        user.save()

        return attrs

        # except DjangoUnicodeDecodeError:
        #     raise serializers.ValidationError('decoding process failed')


class UserIdentitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Identity
        fields = ['identifier_image', 'request_time', 'expire_time', 'status']
        read_only_fields = ['request_time', 'expire_time', 'status']

    def update(self, instance, validated_data):
        super(UserIdentitySerializer, self).update(instance, validated_data)
        instance.request_time = datetime.datetime.now()
        instance.expire_time = None
        instance.status = REQUESTED
        instance.save()
        return instance
