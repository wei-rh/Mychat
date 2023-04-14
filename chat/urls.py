from django.contrib import admin
from django.urls import path

from chat import views

urlpatterns = [
    path('login/', views.Login.as_view(), name="login"),
    path('register/', views.Register.as_view(), name="register"),
    path('list/', views.GetList.as_view(), name="userList"),
]
