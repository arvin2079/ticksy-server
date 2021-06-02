from datetime import timedelta

from django.core.exceptions import ValidationError
from django.views import generic
from ticketing.models import Section
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import add
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from .permissions import IsIdentified, IsOwner, IsTicketOwnerOrTopicOwner, IsSupporterOrOwnerOrTicketCreator
from .swagger import *
from .filters import TicketFilter
from drf_yasg.utils import swagger_auto_schema


class TopicListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TopicsSerializer
    permission_classes = [IsAuthenticated, IsIdentified]
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post']

    @swagger_auto_schema(
        operation_description='Returns a list full of Topics that a user is supporter or creator of them.\nmethod: GET\nurl: /topics',
        responses=get_topics_dictionary_response)
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='Creates a new topic and returns it\'s value.\nmethod: POST\nurl: /topics/',
        responses=post_topics_dictionary_response, request_body=post_topic_dictionary_request_body)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        return Topic.objects.filter((Q(creator=self.request.user) | Q(admins__users__in=[self.request.user])) & Q(
            is_active=True)).distinct().order_by('-id')


class TopicRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = 'id'
    http_method_names = ['get', 'put', 'patch', 'delete']

    @swagger_auto_schema(
        operation_description='Searches for a topic and returns the topic that has a slug exactly matched with the url slug(if exist).\nmethod: GET\nurl: /topics/\<slug\>\nexample: /topics/amoozesh-khu',
        responses=get_topic_dictionary_response)
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='Updates the Topic and returns it\'s value.\nmethod: PATCH\nurl: /topics/\<slug\>\nexample: /topics/amoozesh-khu',
        responses=put_topic_dictionary_response, request_body=put_topic_dictionary_request_body)
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def get_queryset(self):
        return Topic.objects.filter(Q(is_active=True)).distinct()

    @swagger_auto_schema(
        operation_description='Deletes the Topic.\nmethod: DELETE\nurl: /topics/\<slug\>\nexample: /topics/amoozesh-khu',
        responses=delete_topic_dictionary_response)
    def delete(self, request, id):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TopicAdminsListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TopicAdminsSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = None
    http_method_names = ['get', 'post']

    def get_queryset(self):
        topic = get_object_or_404(Topic, id=self.kwargs['id'], is_active=True)
        return Admin.objects.filter(Q(topic=topic)).distinct()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request':request, 'id':self.kwargs['id']})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AdminRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TopicAdminsSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = 'roleid'
    http_method_names = ['get', 'put', 'patch', 'delete']

    def get_object(self):
        return get_object_or_404(Admin, id=self.kwargs['roleid'], topic__id=self.kwargs['id'], topic__is_active=True)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial, context={'id': self.kwargs['id'], 'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, id, roleid):
        instance = self.get_object()
        if Section.objects.filter(Q(admin=instance)):
            ValidationError(message={'message': 'نمیتوان این گروه را حذف کرد چون در یک یا چند زیربخش استفاده شده است.'})
        if Ticket.objects.filter(Q(admin=instance)):
            ValidationError(message={'message': 'نمیتوان این گروه را حذف کرد چون در یک یا چند تیکت استفاده شده است.'})
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SectionListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = SectionsSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    http_method_names = ['get', 'post']

    def get_queryset(self):
        return Section.objects.filter(Q(topic__id=self.kwargs['id']) & Q(is_active=True))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request':request, 'id':self.kwargs['id']})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EmailListAPIView(generics.ListAPIView):
    serializer_class = UserSerializerRestricted
    permission_classes = [IsAuthenticated, IsIdentified]
    search_fields = ['email']
    filter_backends = [filters.SearchFilter]
    pagination_class = None
    http_method_names = ['get']

    @swagger_auto_schema(
        operation_description='Just searchs for 10 first emails containing the searched text.\nmethod: GET\nurl: /email/?search=\<Text\>\nexample: /email/?search=karami',
        responses=get_email_dictionary_response, query_serializer=UserSerializerRestricted)
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        return User.objects.filter(Q(identity__status=IDENTIFIED) & (
                Q(identity__expire_time__isnull=True) | Q(
            identity__expire_time__gt=timezone.now()))).distinct().order_by('-email')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset[:10]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TicketListAPIView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['id', 'title']
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_class = TicketFilter
    http_method_names = ['get']

    @swagger_auto_schema(
        operation_description='Returns a list of Tickets that belong to the user.\nmethod: GET\nurl: /tickets/?search=searchtext&status=1&page=1\nexample: tickets/?search=1&status=2&page=1\nOptional search field in the url, will search on \"id\" and \"title\".\nOptional status, filters the results based on the status field in the model (status can have \{0, 1, 2, 3, 4\} values)\nIn status, 0 means no filter, others mean status field in the model has to be equal to status in the url',
        responses=get_ticket_dictionary_response)
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        return Ticket.objects.filter(creator=self.request.user)


class TicketListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['id', 'title']
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_class = TicketFilter

    @swagger_auto_schema(
        operation_description='Creates a new Ticket and relates it to the Topic that It\'s slug is inserted in the url.\nmethod: POST\nurl: /topics/\<slug\>/tickets/\nexample: /topics/amoozesh-khu/tickets/',
        responses=post_ticket_dictionary_response, request_body=post_ticket_dictionary_request_body)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # todo: validate user
        return super(TicketListCreateAPIView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return Ticket.objects.filter(Q(topic__slug=self.kwargs.get('slug')) & (
                    Q(topic__creator=self.request.user) | Q(topic__supporters__in=[self.request.user])))


class TicketRetriveAPIView(generics.RetrieveAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Ticket.objects.filter(id=self.kwargs.get('id')).first()


class MessageListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsTicketOwnerOrTopicOwner]
    pagination_class = None
    http_method_names = ['get', 'post']

    @swagger_auto_schema(
        operation_description='Returns a list of Messages that belong to the inserted Ticket id.\nmethod: GET\nurl: /tickets/\<id\>\nexample: /tickets/18/',
        responses=get_message_dictionary_response)
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(operation_id='topics_tickets_message_create',
                         operation_description='Creates a new Message and relates it to the Ticket that It\'s id is inserted in the url.\nmethod: POST\nurl: /tickets/\<id\>\nexample: /tickets/18/',
                         responses=post_message_dictionary_response, request_body=post_message_dictionary_request_body)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        return Message.objects.filter(Q(ticket=self.kwargs.get('id'))).distinct().order_by('id')


class MessageUpdateAPIView(generics.UpdateAPIView):
    serializer_class = MessageUpdateSerializer
    permission_classes = [IsAuthenticated, IsIdentified, IsSupporterOrOwnerOrTicketCreator]
    http_method_names = ['patch']
    lookup_field = 'id'

    @swagger_auto_schema(
        operation_description='Updates rate of a Message.\nmethod: PATCH\nurl: message/\<int:id\>/\nexample: message/18/',
        responses=patch_ratemessage_dictionary_response, request_body=patch_ratemessage_dictionary_request_body)
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def get_queryset(self):
        return Message.objects.filter(id=self.kwargs.get('id'))

    def get_object(self):
        return get_object_or_404(self.get_queryset())


class GetRecommendedTopicsAPIView(generics.ListAPIView):
    serializer_class = RecommendedTopicsSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Topic.objects.filter(is_recommended=True)
