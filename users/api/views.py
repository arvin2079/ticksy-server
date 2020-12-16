from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import permissions, generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from ..models import User
from .serializer import UserSerializer,\
    SignupSerializer,\
    ResetPasswordRequestSerializer,\
    ResetPasswordNewPasswordSerializer


class UserInfoApiView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class LoginApiView(ObtainAuthToken):
    authentication_classes = [permissions.AllowAny]  # just for intention be more explicit

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

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordRequest(generics.CreateAPIView):
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'An email has now been sent to your account successfuly'}, status=status.HTTP_200_OK)


class ResetPasswordValidateToken(generics.RetrieveAPIView):

    def get(self, request, uib64, token, *args, **kwargs):
        try:
            user_id = smart_str(urlsafe_base64_decode(uib64))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'detail': 'کاربر با مشخصات وارد شده موجود نمی باشد'},
                                status=status.HTTP_400_BAD_REQUEST)

            return Response({'detail': 'مشخصات معتبر'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail': 'مشخصات نامعبر'}, status=status.HTTP_401_UNAUTHORIZED)
        except DjangoUnicodeDecodeError:
            return Response({'detail': 'decoding process failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ResetPasswordNewPassword(generics.GenericAPIView):
    serializer_class = ResetPasswordNewPasswordSerializer

    def patch(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'detail': 'رمز عبور با موفقیت تغییر یافت'}, status=status.HTTP_200_OK)
