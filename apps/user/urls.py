from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token
from user import views

# 添加jwt下views视图下obtain_jwt_token(登录)
urlpatterns = [
    path('login/', obtain_jwt_token),
    path('info/', views.get_user_info)
]
