from rest_framework import permissions, generics, authentication, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from .serializer import UserSerializer, SignupSerializer


class UserInfoApiView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication,]
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class LoginApiView(ObtainAuthToken):
    authentication_classes = []

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
    authentication_classes = [authentication.TokenAuthentication, ]
    permissions = (permissions.IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

