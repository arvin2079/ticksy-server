from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import permissions, generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..models import User, Identity
from ..permissions import IdentifyPermission
from .serializer import UserSerializer, \
    SignupSerializer, \
    ResetPasswordRequestSerializer, \
    ResetPasswordNewPasswordSerializer, \
    UserIdentitySerializer


class UserInfoApiView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(
        responses={
            401: 'not authenticated or wrong token is used',
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request)


class SigninApiView(ObtainAuthToken):
    permissions = [permissions.AllowAny]  # just for intention be more explicit

    @swagger_auto_schema(
        responses={
            400: 'bad request, make sure you enter the email as username and your true password correctly',
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class SignupApiView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permissions = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        responses={
            400: 'bad request, make sure you fill the neccessary fields correnctly based on field validation '
                 'provided in example value in json format\nvalidations:\n\t- first_name: in persian\n\t'
                 '- last_name: in persian',
            401: 'not authenticated or wrong token is used',
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordRequest(generics.CreateAPIView):
    serializer_class = ResetPasswordRequestSerializer

    @swagger_auto_schema(
        responses={
            400: 'not valid email or email does not exist!',
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'An email has now been sent to your account successfuly'}, status=status.HTTP_200_OK)


class ResetPasswordValidateToken(generics.RetrieveAPIView):

    @swagger_auto_schema(
        responses={
            500: 'possibly unicode decoding failed user have to try the process again',
            401: 'not valid token or uib64 or not authorized yet',
        }
    )
    def get(self, request, uib64, token, *args, **kwargs):
        try:
            user_id = smart_str(urlsafe_base64_decode(uib64))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'detail': 'کاربر با مشخصات وارد شده موجود نمی باشد'},
                                status=status.HTTP_401_UNAUTHORIZED)

            return Response({'detail': 'مشخصات معتبر'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail': 'مشخصات نامعبر'}, status=status.HTTP_401_UNAUTHORIZED)
        except DjangoUnicodeDecodeError:
            return Response({'detail': 'decoding process failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ResetPasswordNewPassword(generics.GenericAPIView):
    serializer_class = ResetPasswordNewPasswordSerializer

    @swagger_auto_schema(
        responses={
            401: 'user is not authenticated or the change password link is not validated for user',
            500: 'possibly unicode decoding failed user have to try the process again',
        }
    )
    def patch(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'detail': 'رمز عبور با موفقیت تغییر یافت'}, status=status.HTTP_200_OK)


class IdentityApiView(generics.RetrieveUpdateAPIView):
    serializer_class = UserIdentitySerializer
    permission_classes = (permissions.IsAuthenticated, IdentifyPermission)

    def get_object(self):
        user = self.request.user
        return Identity.objects.filter(user=user).first()