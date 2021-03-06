from django.http import JsonResponse
from rest_framework_jwt.utils import jwt_decode_handler
from django.contrib.auth import get_user_model


def get_user_info(request):
    if request.method == 'GET' and 'OPTIONS':
        token = request.GET.get('token')
        toke_user = []
        toke_user = jwt_decode_handler(token)
        user_id = toke_user["user_id"]
        data = {
            "code": 200,
            "message": "请求成功"
        }
        return JsonResponse(data)


