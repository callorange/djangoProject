"""
샌드위치 등록/수정/삭제 API View 모듈
"""

__all__ = [
    "SandwichViewSet",
]

from django.db import transaction
from django.db.models import F
from rest_framework import viewsets

from django_filters import rest_framework as dj_filters

from api.models.sandwich import *
from api.serializers.sandwich import *


class SandwichFilter(dj_filters.FilterSet):
    """샌드위치 검색을 위한 django_filters FilterSet"""

    price_min = dj_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = dj_filters.NumberFilter(field_name="price", lookup_expr="lte")

    bread_min = dj_filters.NumberFilter(field_name="bread__price", lookup_expr="gte")
    bread_max = dj_filters.NumberFilter(field_name="bread__price", lookup_expr="lte")

    topping_min = dj_filters.NumberFilter(
        field_name="topping__price", lookup_expr="gte"
    )
    topping_max = dj_filters.NumberFilter(
        field_name="topping__price", lookup_expr="lte"
    )

    cheese_min = dj_filters.NumberFilter(field_name="cheese__price", lookup_expr="gte")
    cheese_max = dj_filters.NumberFilter(field_name="cheese__price", lookup_expr="lte")

    sauce_min = dj_filters.NumberFilter(field_name="sauce__price", lookup_expr="gte")
    sauce_max = dj_filters.NumberFilter(field_name="sauce__price", lookup_expr="lte")

    class Meta:
        model = Sandwich
        fields = []


class SandwichViewSet(viewsets.ModelViewSet):
    """샌드위치 API 관련 뷰셋"""

    queryset = Sandwich.objects.all()
    serializer_class = SandwichInfoSerializer

    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = SandwichFilter

    def get_serializer_class(self):
        """request.method 에 따라서 다른 serializer를 반환한다"""
        if self.request.method in ["POST", "PUT", "PATCH"]:
            return SandwichSerializer
        return self.serializer_class

    @transaction.atomic()
    def perform_create(self, serializer):
        """샌드위치 생성시 재료의 재고 -1"""
        instance = serializer.save()
        instance.bread.update(stock=F("stock") - 1)
        instance.topping.update(stock=F("stock") - 1)
        instance.cheese.update(stock=F("stock") - 1)
        instance.sauce.update(stock=F("stock") - 1)

    def perform_update(self, serializer):
        serializer.save()

    @transaction.atomic()
    def perform_destroy(self, instance):
        """샌드위치 삭제시 재료의 재고 +1"""
        instance.bread.update(stock=F("stock") + 1)
        instance.topping.update(stock=F("stock") + 1)
        instance.cheese.update(stock=F("stock") + 1)
        instance.sauce.update(stock=F("stock") + 1)
        instance.delete()
