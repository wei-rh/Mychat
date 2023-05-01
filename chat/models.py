from django.db import models


# Create your models here.

class User(models.Model):
    phone_number = models.CharField(max_length=255, unique=True, verbose_name="手机号")
    password = models.CharField(max_length=255, unique=False, verbose_name="密码")
    is_active = models.BooleanField(default=True)
    class Meta:
        db_table = "user"
        verbose_name = "用户账号表"
        verbose_name_plural = verbose_name

class CustomToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户id")
    key = models.CharField(max_length=40, unique=True, verbose_name="token值")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    expires_at = models.DateTimeField(verbose_name="过期时间")
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['key']),
        ]
        db_table = "customtoken"
        verbose_name = "token表"
        verbose_name_plural = verbose_name

class ChatHistory(models.Model):
    uid = models.IntegerField(verbose_name="用户id")
    sid = models.IntegerField(verbose_name="会话id")
    user_input = models.TextField(verbose_name="用户提问时间")
    bot_output = models.TextField(verbose_name="gpt响应时间")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    expires_at = models.DateTimeField(verbose_name="响应时间")

    class Meta:
        db_table = "chathistory"
        verbose_name = "会话历史记录"
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['uid']),
            models.Index(fields=['sid']),
        ]