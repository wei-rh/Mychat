import datetime
import json
from django.core import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ChatHistory
import openai


class RecentRecords(APIView):
    def get(self, request):

        page = int(request.GET.get('page', 0))
        print(page)
        uid = request.user.id
        sid = request.data.get('sid', 0)
        start = page * 6
        end = (page + 1) * 6
        chat_history = ChatHistory.objects.filter(sid=sid, uid=uid).order_by('-expires_at')[start:end]
        serialized_data = serializers.serialize('json', chat_history)  # 将 QuerySet 转换为 JSON 格式的字符串
        chat_history = json.loads(serialized_data)
        chat_history = chat_history
        return Response(data={'chat_history': chat_history}, status=200)


class GetLastSid(APIView):
    def get(self, request):
        uid = request.user.id
        print(uid)
        chat_history = ChatHistory.objects.filter(uid=uid).order_by('expires_at')[:1]
        print(chat_history)
        if chat_history:
            sid = chat_history[0].sid
            return Response(data={'sid': sid}, status=200)
        return Response(data={'sid':-1}, status=200)