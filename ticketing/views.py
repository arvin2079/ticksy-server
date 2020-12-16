from django.db.models import Q
from rest_framework import permissions
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Topic
from .serializers import TopicSerializer
from .permissions import IsIdentified


class TopicListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated, IsIdentified]

    def get_queryset(self):
        return Topic.objects.filter(Q(creator=self.request.user) | Q(supporters__in=[self.request.user])).distinct()
