from django.urls import path
from .views import TopicListCreateAPIView, TopicRetrieveUpdateDestroyAPIView, EmailListAPIView, TicketCreateAPIView, \
    MessageListCreateAPIView, MessageUpdateAPIView, GetRecommendedTopicsAPIView, TicketListAPIView

urlpatterns = [
    path('topics/', TopicListCreateAPIView.as_view(), name='topic-list-create'),
    path('topics/<slug:slug>/', TopicRetrieveUpdateDestroyAPIView.as_view(), name='topic-retrieve-update-destroy'),
    path('topics/<slug:slug>/tickets/', TicketCreateAPIView.as_view(), name='ticket-create'),
    path('tickets/', TicketListAPIView.as_view(), name='ticket-list'),
    path('tickets/<int:id>/', MessageListCreateAPIView.as_view(), name='message-list-create'),
    path('message/<int:id>/', MessageUpdateAPIView.as_view(), name='message-rate-update'),
    path('email/', EmailListAPIView.as_view(), name='email-list'),
    path('get-recommended-topics/', GetRecommendedTopicsAPIView.as_view(), name='recommended-topics-list')
]
