from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import status
import inspect


# test
def analyze_class(cls, instance=None):
    print(f"\n🔍 Analyzing {cls.__name__}")

    # --- Class attributes (own + inherited)
    class_attrs = {}
    for base in inspect.getmro(cls):  # walk through MRO
        for k, v in base.__dict__.items():
            if not callable(v) and not k.startswith("__"):
                class_attrs[k] = v
    print("Class attributes:", class_attrs)

    # --- Instance attributes (need an instance)
    if instance:
        print("Instance attributes:", instance.__dict__)

    # --- Instance methods (own + inherited)
    instance_methods = [
        name for name, func in inspect.getmembers(cls, inspect.isfunction)
    ]
    print("Instance methods:", instance_methods)

    # --- Class methods (own + inherited)
    class_methods = []
    for base in inspect.getmro(cls):
        for name, obj in base.__dict__.items():
            if isinstance(obj, classmethod):
                class_methods.append(name)
    print("Class methods:", class_methods)


class TestPagination(PageNumberPagination): ...


class TestLimitOffsetPagination(LimitOffsetPagination): ...


testpagination = TestPagination()
testlimitoffsetpagination = TestLimitOffsetPagination()
analyze_class(PageNumberPagination, testpagination)
analyze_class(LimitOffsetPagination, testlimitoffsetpagination)


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
