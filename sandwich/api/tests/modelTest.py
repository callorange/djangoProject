from decimal import Decimal

from django.db.models import Sum
from django.test import TestCase

from api.models import Ingredient, IngredientType, Sandwich


class ModelTestCase(TestCase):
    """모델 테스트"""

    def setUp(self):
        """데이터 등록"""
        Ingredient.objects.create(name="빵1", stock=100, price=1000)
        Ingredient.objects.create(name="빵2", stock=200, price=1500)
        Ingredient.objects.create(name="토핑", category=IngredientType.TOPPING, stock=55, price=2000)
        Ingredient.objects.create(name="치즈", category=IngredientType.CHEESE, stock=33, price=1500)
        Ingredient.objects.create(name="소스", category=IngredientType.SAUCE, stock=22, price=9900)

    def test_get(self):
        """데이터 확인"""
        # 빵1 데이터 확인
        bread = Ingredient.objects.get(name="빵1")
        self.assertEqual(bread.stock, 100)
        self.assertEqual(bread.price, Decimal("1000"))

        # 빵의 갯수는 2개
        count = Ingredient.objects.filter(category=IngredientType.BREAD).count()
        self.assertEqual(count, 2)

        # 소스의 갯수는 1개
        count = Ingredient.objects.filter(category=IngredientType.SAUCE).count()
        self.assertEqual(count, 1)

    def test_bread(self):
        """빵의 가격 업데이트 확인"""
        bread = Ingredient.objects.get(name="빵1")
        bread.stock = 90
        bread.price = 100
        bread.save()
        bread.refresh_from_db()
        self.assertEqual(bread.stock, 90)
        self.assertEqual(bread.price, 100)
        self.assertEqual(bread.price, Decimal("100"))

    def test_sandwich(self):
        """샌드위치 재료 등록 및 가격 확인"""
        # 재료를 가져온다
        bread = Ingredient.objects.filter(category=IngredientType.BREAD).first()
        topping = Ingredient.objects.filter(category=IngredientType.TOPPING).first()
        cheese = Ingredient.objects.filter(category=IngredientType.CHEESE).first()
        sauce = Ingredient.objects.filter(category=IngredientType.SAUCE).first()

        # 샌드위치 데이터 생성
        sand = Sandwich.objects.create(name="샌드위치1")

        # 재료 등록
        sand.ingredients.add(bread, topping, cheese, sauce)

        # 등록된 재료는 총 4개
        self.assertEqual(sand.ingredients.all().count(), 4)

        # 재료가격 총합은 14900
        self.assertEqual(sand.get_total_price(), 14900)

        # 데이터 생성시 가격 등록안했으므로 가격이 0원이다
        self.assertNotEqual(sand.get_total_price(), sand.price)
        self.assertEqual(sand.price, 0)

        # 가격을 등록 하고 확인해보자
        sand.price = 14900
        self.assertEqual(sand.get_total_price(), sand.price)
