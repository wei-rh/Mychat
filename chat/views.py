from .serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .middlewares import generate_custom_token
from rest_framework import serializers
class NewPassword(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("账号不存在！")

        user.set_password(password)
        user.save()
        return Response(data={"msg":"success"},status=status.HTTP_200_OK)

class Register(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = User.objects.filter(username=username).first()
        if user:
            raise serializers.ValidationError("用户已存在！")
        user = User(username=username)
        user.set_password(password)
        user.save()
        return Response(data={"message": "success"}, status=status.HTTP_200_OK)


class Token_is_valid(APIView):
    def get(self, request):
        # 将所有用户序列化为一个列表
        return Response(data={"valid":True}, status=status.HTTP_200_OK)

