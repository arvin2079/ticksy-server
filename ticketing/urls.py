from django.urls import path
from .views import TopicListCreateAPIView, TopicRetrieveUpdateDestroyAPIView, EmailListAPIView, TicketListCreateAPIView, MessageListCreateAPIView, MessageUpdateAPIView


urlpatterns = [
    path('topics/', TopicListCreateAPIView.as_view(), name='topic-list-create'),
    path('topics/<slug:slug>/', TopicRetrieveUpdateDestroyAPIView.as_view(), name='topic-retrieve-update-destroy'),
    path('topics/<slug:slug>/tickets/', TicketListCreateAPIView.as_view(), name='ticket-list-create'),
    path('topics/<slug:slug>/tickets/<int:id>/', MessageListCreateAPIView.as_view(), name='message-list-create'),
    path('message/<int:id>/', MessageUpdateAPIView.as_view(), name='message-rate-update'),
    path('email/', EmailListAPIView.as_view(), name='email-list')
]
