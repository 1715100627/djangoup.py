import rest_framework_jwt


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user_id': user.id,
        'user_name': user.username,
        'code': 200
    }


def jwt_response_payload_error_handler(serializer, request = None):
    return {
        "msg": "用户名或者密码错误",
        "code": 400,
        "detail": serializer.errors
  }