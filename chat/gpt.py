import datetime

from .serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ChatHistory
from .middlewares import generate_custom_token
import openai

openai.api_key = "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"


class OneChat(APIView):
    def get(self, request):
        use_id = request.user.user_id
        session_id = request.GET.get('sid', 0)
        input_text = request.GET.get('input_text', 0)
        create_time = datetime.datetime.now()
        model = request.data.get("model", 'gpt-3.5-turbo-0301')
        messages = [{"role": "user", "content": input_text}]
        try:
            completion = openai.ChatCompletion.create(
                model= model,
                messages=messages,
                temperature=0.1
            )
        except Exception as e:
            return Response(data={"answer": "请求超时"}, status=500)
        else:
            output_text = completion.choices[0].message.content
            expires_time = datetime.datetime.now()
            chat_history = ChatHistory(uid=use_id,sid=session_id,
                        user_input=input_text, bot_output=output_text,
                        created_at=create_time, expires_at=expires_time)
            chat_history.save()
            return Response(data={"answer":output_text}, status=200)

class MoreChat(APIView):
    pass
