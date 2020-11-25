from rest_framework import permissions, generics, authentication, status
from rest_framework.response import Response

from .serializer import UserSerializer


class UserInfoApiView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    # lookup_field =

    # def get_object(self):

    def get(self, request):
        user = self.request.user
        serializer = UserSerializer(instance=user)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
