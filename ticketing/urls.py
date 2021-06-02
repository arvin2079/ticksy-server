from django.urls import path
from .views import *

urlpatterns = [
    path('topic/', TopicListCreateAPIView.as_view(), name='topic-list-create'),
    path('topic/<int:id>/', TopicRetrieveUpdateDestroyAPIView.as_view(), name='topic-retrieve-update-destroy'),
    path('topic/<int:id>/role/', TopicRolesListCreateAPIView.as_view(), name='topicRoles-list-create'),
    path('topics/<int:id>/tickets/', TicketListCreateAPIView.as_view(), name='ticket-list-create'),
    path('tickets/', TicketListAPIView.as_view(), name='ticket-list'),
    path('tickets/<int:id>/', MessageListCreateAPIView.as_view(), name='message-list-create'),
    path('tickets/<int:id>/get-detail/', TicketRetriveAPIView.as_view(), name='ticket-detail'),
    path('message/<int:id>/', MessageUpdateAPIView.as_view(), name='message-rate-update'),
    path('email/', EmailListAPIView.as_view(), name='email-list'),
    path('get-recommended-topics/', GetRecommendedTopicsAPIView.as_view(), name='recommended-topics-list')
]
