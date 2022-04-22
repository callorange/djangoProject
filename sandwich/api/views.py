__all__ = [
    "BreadViewSet",
    "ToppingViewSet",
    "CheeseViewSet",
    "SauceViewSet",
    "SandwichViewSet",
]

from django.db import transaction
from django.db.models import F, Count
from rest_framework import viewsets, serializers

from django_filters import rest_framework as dj_filters

from api.models.ingredient import *
from api.models.sandwich import *
from api.serializers.ingredient import *
from api.serializers.sandwich import *


class BreadViewSet(viewsets.ModelViewSet):
    """빵 API 뷰셋"""

    queryset = Bread.objects.all()
    serializer_class = BreadSerializer

    @transaction.atomic()
    def perform_update(self, serializer):
        bread = Bread.objects.get(id=self.kwargs["pk"])
        change_price = serializer.validated_data["price"] - bread.price  # 가격변동 체크

        instance = serializer.save()

        if change_price != 0:
            Sandwich.objects.filter(bread__in=[instance.id]).update(
                price=F("price") + change_price
            )

    @transaction.atomic()
    def perform_destroy(self, instance):
        # 빵이 쓰이고 있는 샌드위치 갯수
        use_sandwich = Sandwich.objects.filter(bread__in=[instance.id])

        if use_sandwich.count() > 0:
            sandwich_id = ", ".join([str(obj.id) for obj in use_sandwich])  # 샌드위치 ID
            raise serializers.ValidationError(
                f"샌드위치에 사용중인 빵은 삭제할 수 없습니다. 샌드위치 ID: {sandwich_id}"
            )

        # 샌드위치 가격 업데이트
        use_sandwich.update(price=F("price") - instance.price)

        # 삭제
        instance.delete()


class ToppingViewSet(viewsets.ModelViewSet):
    """토핑 API 뷰셋"""

    queryset = Topping.objects.all()
    serializer_class = ToppingSerializer

    @transaction.atomic()
    def perform_update(self, serializer):
        topping = Topping.objects.get(id=self.kwargs["pk"])
        change_price = serializer.validated_data["price"] - topping.price  # 가격변동 체크

        instance = serializer.save()

        if change_price != 0:
            Sandwich.objects.filter(topping__in=[instance.id]).update(
                price=F("price") + change_price
            )

    @transaction.atomic()
    def perform_destroy(self, instance):
        # 현재 지우려는 토핑을 사용중인 샌드위치 별로 사용중인 토핑 갯수를 구한다.
        # [{id: 1, t_count: 2}...]
        use_sandwich = Sandwich.objects.filter(topping__in=[instance.id])
        use_annotate = (
            Sandwich.objects.filter(id__in=use_sandwich)  # 이렇게 해야 annotate가 제대로 된다 ㅎ
            .values("id")
            .annotate(t_count=Count("topping"))
        )

        # 토핑이 1개뿐인 샌드위치 갯수
        use_count = use_annotate.filter(t_count__lte=1)

        if use_count.count() > 0:
            # 샌드위치 ID. annotate로 가져왔으므로 dict다
            sandwich_id = ", ".join([str(obj["id"]) for obj in use_annotate])
            raise serializers.ValidationError(
                f"샌드위치에 하나뿐인 토핑은 삭제할 수 없습니다. 샌드위치 ID: {sandwich_id}"
            )

        # 샌드위치 가격 업데이트
        use_sandwich.update(price=F("price") - instance.price)

        # 삭제
        instance.delete()


class CheeseViewSet(viewsets.ModelViewSet):
    """치즈 API 뷰셋"""

    queryset = Cheese.objects.all()
    serializer_class = CheeseSerializer

    @transaction.atomic()
    def perform_update(self, serializer):
        cheese = Cheese.objects.get(id=self.kwargs["pk"])
        change_price = serializer.validated_data["price"] - cheese.price  # 가격변동 체크

        instance = serializer.save()

        if change_price != 0:
            Sandwich.objects.filter(cheese__in=[instance.id]).update(
                price=F("price") + change_price
            )

    @transaction.atomic()
    def perform_destroy(self, instance):
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


class SauceViewSet(viewsets.ModelViewSet):
    """소스 API 뷰셋"""

    queryset = Sauce.objects.all()
    serializer_class = SauceSerializer

    @transaction.atomic()
    def perform_update(self, serializer):
        sauce = Sauce.objects.get(id=self.kwargs["pk"])
        change_price = serializer.validated_data["price"] - sauce.price  # 가격변동 체크

        instance = serializer.save()

        if change_price != 0:
            Sandwich.objects.filter(sauce__in=[instance.id]).update(
                price=F("price") + change_price
            )

    @transaction.atomic()
    def perform_destroy(self, instance):
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
        instance = serializer.save()
        instance.bread.update(stock=F("stock") - 1)
        instance.topping.update(stock=F("stock") - 1)
        instance.cheese.update(stock=F("stock") - 1)
        instance.sauce.update(stock=F("stock") - 1)

    def perform_update(self, serializer):
        serializer.save()

    @transaction.atomic()
    def perform_destroy(self, instance):
        instance.bread.update(stock=F("stock") + 1)
        instance.topping.update(stock=F("stock") + 1)
        instance.cheese.update(stock=F("stock") + 1)
        instance.sauce.update(stock=F("stock") + 1)
        instance.delete()
