from django.urls import path
from .views import UserInfoApiView

app_name = 'users'

urlpatterns = [
    path('info/', UserInfoApiView.as_view(), name='user-info')
]

