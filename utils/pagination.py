from rest_framework.pagination import PageNumberPagination
import rest_framework_jwt
from rest_framework.response import Response


class PageNumberPaginationManual(PageNumberPagination):
    # 默认第几页p,默认两条数据
    page_query_param = 'page'  # 页数
    page_size = 20

    page_size_query_param = 'size'  # 每页数量
    max_page_size = 50  # 前端最大指定

    def get_paginated_response(self, data):
        return Response({
            "code": 200,
            "count": self.page.paginator.count,
            "data": {"data": data},
            "message": "OK",
        })
