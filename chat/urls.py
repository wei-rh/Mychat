from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from chat import views,gpt, chathistory
from chat.utils.Authentication import MyTokenObtainPairView


urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name="login"),
    path('newpass/', views.NewPassword.as_view(), name="newpass"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('register/', views.Register.as_view(), name="register"),
    path('verify/', TokenVerifyView.as_view(), name="token_verify"),
    path('onechat/', gpt.OneChat.as_view(), name="OneChat"),
    path('onechatstream/', gpt.OneChatStream.as_view(), name="OneChatStream"),
    path('recentrecords/', chathistory.RecentRecords.as_view(), name="recentrecords"),
    path('getlastsid/', chathistory.GetLastSid.as_view(), name="getlastsid"),
]
