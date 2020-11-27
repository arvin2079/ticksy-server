from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('info/', UserInfoApiView.as_view(), name='user-info'),
    path('signin/', LoginApiView.as_view(), name='user-signin'),
    path('signup/', SignupApiView.as_view(), name='user-signup')
]

