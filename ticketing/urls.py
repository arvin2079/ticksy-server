from django.urls import path
from .views import TopicList


urlpatterns = [
    path('topics/', TopicList.as_view())
]
