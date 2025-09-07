from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status


class CustomEmployeePagination(PageNumberPagination):
    page_size = 3
    page_query_param = "employee"

    def get_paginated_response(self, data):
        return Response(
            {
                "results": data,
                "results_count": len(data),
                "has_more": self.page.has_next(),
                "total": self.page.paginator.count,
            },
            status=status.HTTP_200_OK,
        )


class CustomBlogPagination(PageNumberPagination):
    page_size = 3
    page_query_param = "blog"

    def get_paginated_response(self, data):
        return Response(
            {
                "results": data,
                "results_count": len(data),
                "has_more": self.page.has_next(),
                "total": self.page.paginator.count,
            },
            status=status.HTTP_200_OK,
        )
