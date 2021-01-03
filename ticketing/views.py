from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import permissions, status, generics, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from users.models import IDENTIFIED
from users.serializers import UserSerializerRestricted
from users.models import User
from datetime import timedelta
from .models import Topic, DEACTIVE
from .serializers import TopicsSerializer, TopicSerializer
from .permissions import IsIdentified, IsOwner


class TopicListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TopicsSerializer
    permission_classes = [IsAuthenticated, IsIdentified]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Topic.objects.filter((Q(creator=self.request.user) | Q(supporters__in=[self.request.user])) & Q(is_active='1')).distinct()

class TopicRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated, IsIdentified, IsOwner]
    lookup_field = 'slug'
    allowed_methods = ['GET', 'PUT', 'DELETE']

    def get_queryset(self):
        return Topic.objects.filter((Q(creator=self.request.user) | Q(supporters__in=[self.request.user])) & Q(is_active='1')).distinct()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
        obj = get_object_or_404(queryset, **filter_kwargs)
        return obj

    def delete(self, request, slug=None):
        instance = self.get_object()
        instance.is_active = DEACTIVE
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EmailListAPIView(generics.ListAPIView):
    serializer_class = UserSerializerRestricted
    permission_classes = [IsAuthenticated, IsIdentified]
    search_fields = ['email']
    filter_backends = [filters.SearchFilter]
    pagination_class = None

    def get_queryset(self):
        start_date = timezone.now()
        end_date = start_date + timedelta(weeks=48*4) # 4 years
        return User.objects.filter(Q(identity__expire_time__range=[start_date, end_date]) & Q(identity__status=IDENTIFIED) & Q(is_staff=True)).distinct().order_by('-email')

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset[:10]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)