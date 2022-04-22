"""
샌드위치 재료 관련 모델

필드가 크게 다를 필요는 없을것 같아서 abstract 모델(Ingredient)을 상속받아 구현
"""

__all__ = ["Bread", "Topping", "Cheese", "Sauce"]

from django.core.validators import MinValueValidator
from django.db import models


class Ingredient(models.Model):
    """재료 추상화 모델"""

    name = models.CharField(
        "이름", unique=True, max_length=100, help_text="100자 이내. 중복 불가"
    )
    stock = models.PositiveIntegerField(
        "재고", default=0, validators=[MinValueValidator(0)], help_text="재고수량"
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
    created_at = models.DateTimeField("등록일", auto_now_add=True, help_text="등록일")
    updated_at = models.DateTimeField("수정일", auto_now=True, help_text="수정일")

    class Meta:
        abstract = True
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Bread(Ingredient):
    class Meta(Ingredient.Meta):
        verbose_name = "빵"
        verbose_name_plural = "빵 리스트"


class Topping(Ingredient):
    class Meta(Ingredient.Meta):
        verbose_name = "토핑"
        verbose_name_plural = "토핑 리스트"


class Cheese(Ingredient):
    class Meta(Ingredient.Meta):
        verbose_name = "치즈"
        verbose_name_plural = "치즈 리스트"


class Sauce(Ingredient):
    class Meta(Ingredient.Meta):
        verbose_name = "소스"
        verbose_name_plural = "소스 리스트"
