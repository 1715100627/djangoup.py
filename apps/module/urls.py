from module import views
from rest_framework import routers

# 创建路由对象
# router = routers.SimpleRouter()
router = routers.DefaultRouter()
# 注册路由
# 1.路由前缀 2.视图集
router.register(r'module', views.ModularViewSet)
router.register(r'moduleadd', views.CreateModularViewSet)
urlpatterns = [
]
urlpatterns += router.urls
