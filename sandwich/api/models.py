from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum


class IngredientType(models.TextChoices):
    BREAD = "BR", "빵"
    TOPPING = "TO", "토핑"
    CHEESE = "CH", "치즈"
    SAUCE = "SA", "소스"


class Ingredient(models.Model):
    """재료 모델"""

    name = models.CharField(
        "이름", unique=True, max_length=100, help_text="100자 이내. 중복 불가"
    )
    category = models.CharField(
        "종류",
        max_length=2,
        choices=IngredientType.choices,
        default=IngredientType.BREAD,
    )
    stock = models.PositiveIntegerField("재고", default=0, help_text="재고수량")
    price = models.DecimalField(
        "가격",
        max_digits=12,
        decimal_places=2,
        blank=True,
        default=0,
        validators=[MinValueValidator(0)],
        help_text="가격. 0원 이상",
    )
    created_at = models.DateTimeField("등록일", auto_now_add=True, help_text="등록일")
    updated_at = models.DateTimeField("수정일", auto_now=True, help_text="수정일")

    class Meta:
        ordering = ["-id"]
        verbose_name = "샌드위치"
        verbose_name_plural = "샌드위치 리스트"

    def __str__(self):
        return self.name


class Sandwich(models.Model):
    """샌드위치 모델"""

    name = models.CharField(
        "이름", unique=True, max_length=100, help_text="100자 이내. 중복 불가"
    )
    description = models.TextField(
        "상세", blank=True, max_length=200, help_text="상세내용. 200자 이내"
    )
    price = models.DecimalField(
        "가격",
        max_digits=12,
        decimal_places=2,
        blank=True,
        default=0,
        validators=[MinValueValidator(0)],
        help_text="가격. 0원 이상",
    )
    ingredients = models.ManyToManyField(Ingredient)
    created_at = models.DateTimeField("등록일", auto_now_add=True, help_text="등록일")
    updated_at = models.DateTimeField("수정일", auto_now=True, help_text="수정일")

    class Meta:
        ordering = ["-id"]
        verbose_name = "샌드위치"
        verbose_name_plural = "샌드위치 리스트"

    def __str__(self):
        return self.name

    def get_total_price(self):
        """재료가격 합계"""
        return self.ingredients.aggregate(Sum('price'))["price__sum"]
