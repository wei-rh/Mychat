from .serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .middlewares import generate_custom_token

class Login(APIView):
    def post(self, request):

        user_list = User.objects.filter(phone_number=request.data["phone_number"],
                                   password=request.data["password"])
        if user_list:
            token = generate_custom_token(user_list[0])
            return Response(data={"token":token}, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

class Register(APIView):
    def post(self, request):
        us = UserSerializer(data=request.data)
        if us.is_valid():
            us.save()
            return Response(data={"message": "success"}, status=status.HTTP_200_OK)
        return Response(us.errors, status=status.HTTP_200_OK)


class Token_is_valid(APIView):
    def get(self, request):
        # 将所有用户序列化为一个列表
        return Response(data={"valid":True}, status=status.HTTP_200_OK)
