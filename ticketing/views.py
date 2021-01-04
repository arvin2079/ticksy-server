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
from .swagger import get_email_dictionary_response, delete_topic_dictionary_response, get_topic_dictionary_response, get_topics_dictionary_response, post_topics_dictionary_response, put_topic_dictionary_response, put_topic_dictionary_request_body, post_topic_dictionary_request_body
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class TopicListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TopicsSerializer
    permission_classes = [IsAuthenticated, IsIdentified]
    pagination_class = PageNumberPagination

    @swagger_auto_schema(operation_description='Returns a list full of Topics that a user is supporter or creator of them.\nmethod: GET\nurl: /topics', responses=get_topics_dictionary_response)
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description='Creates a new topic and returns it\'s value.\nmethod: POST\nurl: /topics/', responses=post_topics_dictionary_response, request_body=post_topic_dictionary_request_body)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        return Topic.objects.filter((Q(creator=self.request.user) | Q(supporters__in=[self.request.user])) & Q(is_active='1')).distinct()

class TopicRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated, IsIdentified, IsOwner]
    lookup_field = 'slug'
    allowed_methods = ['GET', 'PUT', 'DELETE']

    @swagger_auto_schema(operation_description='Searches for a topic and returns the topic that has a slug exactly matched with the url slug(if exist).\nmethod: GET\nurl: /topics/\{slug\}\nexample: /topics/amoozesh-khu', responses=get_topic_dictionary_response)
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description='Updates the Topic and returns it\'s value.\nmethod: PUT\nurl: /topics/\{slug\}\nexample: /topics/amoozesh-khu', responses=put_topic_dictionary_response, request_body=put_topic_dictionary_request_body)
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def get_queryset(self):
        return Topic.objects.filter((Q(creator=self.request.user) | Q(supporters__in=[self.request.user])) & Q(is_active='1')).distinct()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
        obj = get_object_or_404(queryset, **filter_kwargs)
        return obj

    @swagger_auto_schema(operation_description='Deletes the Topic.\nmethod: DELETE\nurl: /topics/\{slug\}\nexample: /topics/amoozesh-khu', responses=delete_topic_dictionary_response)
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

    @swagger_auto_schema(operation_description='Just searchs for 10 first emails containing the searched text.\nmethod: GET\nurl: /email/?search=\{Text\}\nexample: /email/?search=karami', responses=get_email_dictionary_response, query_serializer=UserSerializerRestricted)
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        start_date = timezone.now()
        end_date = start_date + timedelta(weeks=48*4) # 4 years
        return User.objects.filter(Q(identity__expire_time__range=[start_date, end_date]) & Q(identity__status=IDENTIFIED) & Q(is_staff=True)).distinct().order_by('-email')
    
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset[:10]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)