import rest_framework_jwt


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'userInfo': {
            'user_id': user.id,
            'user_name': user.username,
            'roles': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        },
        'code': 200
    }


def jwt_response_payload_error_handler(serializer, request = None):
    return {
        "msg": "用户名或者密码错误",
        "code": 400,
        "detail": serializer.errors
  }