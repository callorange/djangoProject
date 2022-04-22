__all__ = ["BreadViewSet", "ToppingViewSet", "CheeseViewSet", "SauceViewSet"]

from rest_framework import viewsets

from api.models import Ingredient, IngredientType
from api.serializers import IngredientSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    """
    재료 API 관련 부모클래스
    ingredient_type에 재료타입을 지정하면 관련 쿼리셋 리턴 및 저장시 해당 타입 추가 지정
    """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    ingredient_type = None  # 실제 저장될 재료 타입.

    def get_queryset(self):
        if self.ingredient_type:
            return self.queryset.filter(category=self.ingredient_type)
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(category=self.ingredient_type)


class BreadViewSet(IngredientViewSet):
    """빵 API 뷰셋"""

    ingredient_type = IngredientType.BREAD


class ToppingViewSet(IngredientViewSet):
    """토핑 API 뷰셋"""

    ingredient_type = IngredientType.TOPPING


class CheeseViewSet(IngredientViewSet):
    """치즈 API 뷰셋"""

    ingredient_type = IngredientType.CHEESE


class SauceViewSet(IngredientViewSet):
    """소스 API 뷰셋"""

    ingredient_type = IngredientType.SAUCE
