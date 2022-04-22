"""
치즈 등록/수정/삭제 API View 모듈
"""

__all__ = [
    "CheeseViewSet",
]

from django.db import transaction
from django.db.models import F
from rest_framework import viewsets, serializers

from api.models.ingredient import *
from api.models.sandwich import *
from api.serializers.ingredient import *


class CheeseViewSet(viewsets.ModelViewSet):
    """치즈 API 뷰셋"""

    queryset = Cheese.objects.all()
    serializer_class = CheeseSerializer

    @transaction.atomic()
    def perform_update(self, serializer):
        """업데이트시 가격변동이 있을경우 샌드위치 가격 변경"""
        cheese = Cheese.objects.get(id=self.kwargs["pk"])
        change_price = serializer.validated_data["price"] - cheese.price  # 가격변동 체크

        instance = serializer.save()

        if change_price != 0:
            Sandwich.objects.filter(cheese__in=[instance.id]).update(
                price=F("price") + change_price
            )

    @transaction.atomic()
    def perform_destroy(self, instance):
        """치즈 삭제
        1. 샌드위치에 사용 중인 치즈면 오류 응답
        2. 삭제 성공시 가격 업데이트
        * 샌드위치에 치즈는 무조건 1개 이기 때문에 불편함\
          - 샌드위치를 삭제하거나 샌드위치의 치즈를 변경하거나.
        """
        # 치즈가 쓰이고 있는 샌드위치 갯수
        use_sandwich = Sandwich.objects.filter(cheese__in=[instance.id])

        if use_sandwich.count() > 0:
            sandwich_id = ", ".join([str(obj.id) for obj in use_sandwich])  # 샌드위치 ID
            raise serializers.ValidationError(
                f"샌드위치에 사용중인 치즈는 삭제할 수 없습니다. 샌드위치 ID: {sandwich_id}"
            )

        # 샌드위치 가격 업데이트
        use_sandwich.update(price=F("price") - instance.price)

        # 삭제
        instance.delete()
