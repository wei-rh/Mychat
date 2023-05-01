from django.contrib import admin
from django.urls import path

from chat import views,gpt, chathistory

urlpatterns = [
    path('login/', views.Login.as_view(), name="login"),
    path('register/', views.Register.as_view(), name="register"),
    path('is_token/', views.Token_is_valid.as_view(), name="userList"),
    path('onechat/', gpt.OneChat.as_view(), name="OneChat"),
    path('recentrecords/', chathistory.RecentRecords.as_view(), name="recentrecords"),
    path('getlastsid/', chathistory.GetLastSid.as_view(), name="getlastsid"),
]
