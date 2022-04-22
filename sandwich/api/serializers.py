__all__ = [
    "BreadSerializer",
    "ToppingSerializer",
    "CheeseSerializer",
    "SauceSerializer",
    "SandwichInfoSerializer",
    "SandwichSerializer",
]

from rest_framework import serializers

from api.models import *


class IngredientSerializer(serializers.ModelSerializer):
    """
    샌드위치 재료 시리얼라이저
    상속을 통해 세부 사항 구현
    """

    class Meta:
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

    ingredients = IngredientSerializer(many=True, read_only=True)

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

    def validate(self, data):
        """
        Check that start is before finish.
        """
        ingredients = data["ingredients"]

        # for ingredient in ingredients:
        if False:
            raise serializers.ValidationError("finish must occur after start")
        return data
