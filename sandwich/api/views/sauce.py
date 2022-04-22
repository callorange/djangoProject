"""
소스 등록/수정/삭제 API View 모듈
"""

__all__ = [
    "SauceViewSet",
]

from django.db import transaction
from django.db.models import F, Count
from rest_framework import viewsets, serializers


from api.models.ingredient import *
from api.models.sandwich import *
from api.serializers.ingredient import *


class SauceViewSet(viewsets.ModelViewSet):
    """소스 API 뷰셋"""

    queryset = Sauce.objects.all()
    serializer_class = SauceSerializer

    @transaction.atomic()
    def perform_update(self, serializer):
        """업데이트시 가격변동이 있을경우 샌드위치 가격 변경"""
        sauce = Sauce.objects.get(id=self.kwargs["pk"])
        change_price = serializer.validated_data["price"] - sauce.price  # 가격변동 체크

        instance = serializer.save()

        if change_price != 0:
            Sandwich.objects.filter(sauce__in=[instance.id]).update(
                price=F("price") + change_price
            )

    @transaction.atomic()
    def perform_destroy(self, instance):
        """토핑 삭제
        1. 샌드위치에 사용 중인 토핑이면서 토핑이 1개뿐인 경우가 있으면 오류 응답
        2. 삭제 성공시 가격 업데이트
        """
        # 현재 지우려는 소스를 사용중인 샌드위치 별로 사용중인 소스 갯수를 구한다.
        # [{id: 1, s_count: 2}...]
        use_sandwich = Sandwich.objects.filter(sauce__in=[instance.id])
        use_annotate = (
            Sandwich.objects.filter(id__in=use_sandwich)  # 이렇게 해야 annotate가 제대로 된다 ㅎ
            .values("id")
            .annotate(s_count=Count("topping"))
        )

        # 소스가 1개뿐인 샌드위치 갯수
        use_count = use_annotate.filter(s_count__lte=1)

        if use_count.count() > 0:
            # 샌드위치 ID. annotate로 가져왔으므로 dict다
            sandwich_id = ", ".join([str(obj["id"]) for obj in use_annotate])
            raise serializers.ValidationError(
                f"샌드위치에 하나뿐인 치즈는 삭제할 수 없습니다. 샌드위치 ID: {sandwich_id}"
            )

        # 샌드위치 가격 업데이트
        use_sandwich.update(price=F("price") - instance.price)

        # 삭제
        instance.delete()
