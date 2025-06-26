# Django REST Framework
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

class MotorcycleTabulatorLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5
    max_limit = 25
    def get_paginated_response(self, data):
        return Response({
            "data": data,
            "last_page": (self.count // self.limit) + (1 if self.count % self.limit else 0),
            "total": self.count,
        })