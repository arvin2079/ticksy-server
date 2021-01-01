from django.urls import path
from .views import TopicListCreateAPIView, TopicRetrieveUpdateDestroyAPIView, EmailListAPIView


urlpatterns = [
    path('topics/', TopicListCreateAPIView.as_view(), name='topic-list-create'),
    path('topics/<slug:slug>', TopicRetrieveUpdateDestroyAPIView.as_view(), name='topic-retrieve-update-destroy'),
    path('email/', EmailListAPIView.as_view(), name='email-list')
]
