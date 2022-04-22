"""
샌드위치 재료 관련 시리얼라이저 패키지

모델과 마찬가지로 abstract 시리얼라이저를 상속받아 구현했다
"""

__all__ = [
    "BreadSerializer",
    "ToppingSerializer",
    "CheeseSerializer",
    "SauceSerializer",
]


from rest_framework import serializers

from api.models.ingredient import *


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
