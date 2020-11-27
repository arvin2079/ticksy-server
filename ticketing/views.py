from rest_framework import permissions
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Topic
from .serializers import TopicSerializer
from .permissions import Identified


class TopicList(generics.ListCreateAPIView):
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated, Identified]

    def get_queryset(self):
        return Topic.objects.filter(creator=self.request.user)
