import datetime
import random
import string
from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import ObjectDoesNotExist
from chat.models import CustomToken
from django.http import JsonResponse


def generate_custom_token(user, expiration_minutes=60):
    """
    :param user: 传入一个用户
    :param expiration_minutes: 设置token过期时间默认是60分钟
    :return: 返回一个CustomToken对象,取其中的key，也就是token值
    """
    key = ''.join(random.choices(string.ascii_letters + string.digits, k=40))
    expires_at = datetime.datetime.now() + datetime.timedelta(minutes=expiration_minutes)
    token, _ = CustomToken.objects.update_or_create(user=user, defaults={"key": key, "expires_at": expires_at})
    return token.key

def validate_token(key):
    # 这里可以添加具体的验证逻辑，如检查是否过期、是否有效等
    key = key.split()[1]
    try:
        token = CustomToken.objects.get(key=key)
        if token.expires_at < datetime.datetime.now():
            return False
        return True
    except ObjectDoesNotExist:
        return False


class CustomTokenMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info.lstrip('/')

        # 根据路径中是否包含 login 或 register 判断是否需要进行 Token 验证
        if 'login' in path or 'register' in path:
            response = self.get_response(request)
            return response

        # 获取 Authorization header 中的 token
        token = request.headers.get('Authorization', None)

        if not token:
            return JsonResponse({'message': 'Token not provided.'}, status=400)

        # 假设 token 为简单的字符串类型
        is_token_valid = validate_token(token)

        if not is_token_valid:
            return JsonResponse({'message': 'Token is invalid or expired.'}, status=401)

            # 如果 Token 有效，则继续请求
        response = self.get_response(request)

        return response
