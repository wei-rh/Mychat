from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers
from chat.models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    自定义登录认证，使用自有用户表
    username、password这两个字段为必传字段因为 DRF 要检查这些字段是否有效
    username_field = 'phone_number'  这是重命名了，username必传字段设置为了phone_number字段必传
    phone_number = serializers.CharField(required=False) # 这个是设置了自定义的字段是否必传
    """

    def validate(self, attrs):
        # self.context['request'].data 中包含了所有前端出过来的参数
        username = attrs.get("username")
        password = attrs.get("password")

        if not username or not password:
            raise serializers.ValidationError("phone_number and password are required")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("账号不存在！")
        if not user.check_password(password):
            raise serializers.ValidationError("密码不正确！")

        refresh = self.get_token(user)
        data = {"token": str(refresh.access_token), "refresh": str(refresh),
                'is_vip': user.is_vip}
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
