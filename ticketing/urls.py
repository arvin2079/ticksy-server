from django.urls import path
from .views import *

urlpatterns = [
    path('topic/', TopicListCreateAPIView.as_view(), name='topic-list-create'),
    path('topic/<int:id>/', TopicRetrieveUpdateDestroyAPIView.as_view(), name='topic-retrieve-update-destroy'),
    path('topic/<int:id>/role/', TopicAdminsListCreateAPIView.as_view(), name='topicAdmins-list-create'),
    path('topic/<int:id>/get-all-users/', TopicUsersListAPIView.as_view(), name='topicUsers-list'),
    path('topic/<int:id>/role/<int:roleid>/', AdminRetrieveUpdateDestroyAPIView.as_view(), name='role-retrieve-update-destroy'),
    path('topic/<int:id>/category/', SectionListCreateAPIView.as_view(), name='section-list-create'),
    path('topic/<int:id>/category/<int:secid>/', SectionRetrieveUpdateDestroyAPIView.as_view(), name='section-retrieve-update-destroy'),
    path('ticket/', TicketListCreateAPIView.as_view(), name='ticket-list-create'),
    path('ticket/<int:id>/', TicketRetrieveUpdateAPIView.as_view(), name='ticket-retrieve-update'),
    path('ticket/<int:id>/message/', MessageCreateAPIView.as_view(), name='ticket-create'),
    path('message/<int:id>/', MessageUpdateAPIView.as_view(), name='message-rate-update'),
    path('all-topics/', TopicsListAPIView.as_view(), name='all-topics'),
    path('email/', EmailListAPIView.as_view(), name='email-list'),
    path('get-recommended-topics/', GetRecommendedTopicsAPIView.as_view(), name='recommended-topics-list')
]
