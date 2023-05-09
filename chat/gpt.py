import datetime

from django.http import StreamingHttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ChatHistory
import openai
from rest_framework import serializers
openai.api_key = "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"

class OneChat(APIView):
    def post(self, request):
        use_id = request.user.id
        session_id = request.data.get('sid', 0)
        input_text = request.data.get('input_text', 0)
        history_page = request.data.get('history_page', 5)
        is_stream = request.data.get('is_stream', False)
        print(use_id, session_id, input_text, history_page, is_stream)
        messages = []
        if is_stream:
            chat_history = ChatHistory.objects.filter(sid=session_id, uid=use_id).order_by('-expires_at')[0:history_page]
            for chat in chat_history[::-1]:
                messages.append({"role": "user", "content": chat.user_input})
                messages.append({"role": "assistant", "content": chat.bot_output})
        create_time = datetime.datetime.now()
        model = request.data.get("model", 'gpt-3.5-turbo-0301')
        messages.append({"role": "user", "content": input_text})
        try:
            completion = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=0.1
            )
        except Exception as e:
            raise serializers.ValidationError("请求超时！")
        else:
            output_text = completion.choices[0].message.content
            expires_time = datetime.datetime.now()
            chat_history = ChatHistory(uid=use_id, sid=session_id,
                                       user_input=input_text, bot_output=output_text,
                                       created_at=create_time, expires_at=expires_time)
            chat_history.save()
            return Response(data={"answer": output_text}, status=200)

class OneChatStream(APIView):
    def post(self, request):
        use_id = request.user.id
        session_id = request.data.get('sid', 0)
        input_text = request.data.get('input_text', 0)
        create_time = datetime.datetime.now()
        history_page = request.data.get('history_page', 5)
        is_history = request.data.get('is_history', False)
        messages = []
        if is_history:
            chat_history = ChatHistory.objects.filter(sid=session_id, uid=use_id).order_by('-expires_at')[
                           0:history_page]
            for chat in chat_history[::-1]:
                messages.append({"role": "user", "content": chat.user_input})
                messages.append({"role": "assistant", "content": chat.bot_output})
        model = request.data.get("model", 'gpt-3.5-turbo-0301')
        messages.append({"role": "user", "content": input_text})
        try:
            completion = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=0.1,
                stream=True
            )
        except Exception as e:
            return Response(data={"answer": "请求超时"}, status=500)
        else:
            expires_time = datetime.datetime.now()
            chat_history = ChatHistory(uid=use_id, sid=session_id,
                                       user_input=input_text, bot_output='',
                                       created_at=create_time, expires_at=expires_time)
            output = ''
            def content_stream():
                nonlocal output
                nonlocal chat_history
                for r in completion:
                    if 'content' in r.choices[0].delta.keys():
                        print(r.choices[0].delta['content'])
                        output += r.choices[0].delta['content']
                        yield r.choices[0].delta['content']
                    else:
                        chat_history.bot_output = output
                        chat_history.save()
            return StreamingHttpResponse(content_stream(), status=200)
