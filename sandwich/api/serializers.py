__all__ = [
    "BreadSerializer",
    "ToppingSerializer",
    "CheeseSerializer",
    "SauceSerializer",
    "SandwichInfoSerializer",
    "SandwichSerializer",
]

from decimal import Decimal

from django.db import transaction
from rest_framework import serializers

from api.models import *


class IngredientSerializer(serializers.ModelSerializer):
    """
    샌드위치 재료 시리얼라이저
    상속을 통해 세부 사항 구현
    """

    class Meta:
        abstract = True
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class BreadSerializer(IngredientSerializer):
    """빵 시리얼라이저"""

    class Meta(IngredientSerializer.Meta):
        model = Bread


class ToppingSerializer(IngredientSerializer):
    """토핑 시리얼라이저"""

    class Meta(IngredientSerializer.Meta):
        model = Topping


class CheeseSerializer(IngredientSerializer):
    """치즈 시리얼라이저"""

    class Meta(IngredientSerializer.Meta):
        model = Cheese


class SauceSerializer(IngredientSerializer):
    """소스 시리얼라이저"""

    class Meta(IngredientSerializer.Meta):
        model = Sauce


class SandwichInfoSerializer(serializers.ModelSerializer):
    "샌드위치 상세정보 시리얼라이저"

    bread = BreadSerializer(many=True, read_only=True)
    topping = ToppingSerializer(many=True, read_only=True)
    cheese = CheeseSerializer(many=True, read_only=True)
    sauce = SauceSerializer(many=True, read_only=True)

    class Meta:
        model = Sandwich
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class SandwichSerializer(serializers.ModelSerializer):
    "샌드위치 등록/수정 시리얼라이저"

    class Meta:
        model = Sandwich
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def count_check(self, obj: list, min: int = 1, max: int = 1, name: str = ""):
        """갯수 체크 함수

        Parameters
        ----------
        obj : list
            validate_Foo 함수에서 넘긴 갯수를 체크해야하는 리스트
        min : int
            최소갯수
        max : int
            최대갯수
        name : str
            오류문구에 들어갈 검사항목의 이름
        """
        count = len(obj)
        if count < min:
            raise serializers.ValidationError(f"{name}: {min}개 이상 선택하셔야 합니다.")
        if count > max:
            raise serializers.ValidationError(f"{name}: {max}개까지만 선택가능 합니다.")

    def validate_bread(self, value):
        """빵: 1개"""
        # 수량체크
        self.count_check(value, name="빵")

        # DB 체크 및 재고 체크
        for target in value:
            if target.stock == 0:
                raise serializers.ValidationError(f"재고가 없는 빵을 선택하셨습니다.")

        return value

    def validate_topping(self, value):
        """토핑: 1~2개"""
        # 수량체크
        self.count_check(value, max=2, name="토핑")

        # DB 체크 및 재고 체크
        for target in value:
            if target.stock == 0:
                raise serializers.ValidationError("재고가 없는 토핑을 선택하셨습니다.")
            
        return value

    def validate_cheese(self, value):
        """치즈: 1개"""
        # 수량체크
        self.count_check(value, max=1, name="치즈")
        
        # DB 체크 및 재고 체크
        for target in value:
            if target.stock == 0:
                raise serializers.ValidationError("재고가 없는 치즈를 선택하셨습니다.")
            
        return value

    def validate_sauce(self, value):
        """소스: 1~2개"""
        # 수량체크
        self.count_check(value, max=2, name="소스")
        
        # DB 체크 및 재고 체크
        for target in value:
            if target.stock == 0:
                raise serializers.ValidationError("재고가 없는 소스를 선택하셨습니다.")
            
        return value

    def validate(self, data):
        """샌드위치 가격 업데이트"""
        price = sum(o.price for o in data['bread'])
        price += sum(o.price for o in data['topping'])
        price += sum(o.price for o in data['cheese'])
        price += sum(o.price for o in data['sauce'])
        data["price"] = Decimal(str(price))
        return data

