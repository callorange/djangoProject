__all__ = ["IngredientSerializer"]

from rest_framework import serializers

from api.models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """샌드위치 재료 시리얼라이저"""

    class Meta:
        model = Ingredient
        # fields = '__all__'
        exclude = ["category"]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]
