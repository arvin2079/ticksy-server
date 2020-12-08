from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('info/', UserInfoApiView.as_view(), name='user_info'),
    path('signin/', LoginApiView.as_view(), name='user_signin'),
    path('signup/', SignupApiView.as_view(), name='user_signup'),
    path('reset_password/request/', ResetPasswordRequest.as_view(), name='reset_password_request'),
    path('reset_password/confirm-credential/<str:uib64>/<str:token>', ResetPasswordValidateToken.as_view(),
         name='reset_password_confirm_credential'),
    path('reset_password/new-password/', ResetPasswordNewPassword.as_view(), name='reset_password_new_password'),
]

