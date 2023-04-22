from .serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .middlewares import generate_custom_token

class Login(APIView):
    def post(self, request):
        try:
            user = User.objects.get(phone_number=request.data["phone_number"],
                                    password=request.data["password"])
        except User.DoesNotExist:
            return Response(data={"message":"error"}, status=401)
        else:
            token = generate_custom_token(user)
            return Response(data={"token":token, "message":"success"}, status=status.HTTP_200_OK)


class Register(APIView):
    def post(self, request):
        us = UserSerializer(data=request.data)
        if us.is_valid():
            us.save()
            return Response(data={"message": "success"}, status=status.HTTP_200_OK)
        return Response(us.errors, status=status.HTTP_200_OK)


class GetList(APIView):
    def get(self, request):
        print(request.user, type(request.user))
        s = UserSerializer(instance=User.objects.all(), many=True)
        # 将所有用户序列化为一个列表
        return Response(data=s.data, status=status.HTTP_200_OK)
