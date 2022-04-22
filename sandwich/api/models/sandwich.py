"""
샌드위치 관련 모델
"""


__all__ = ["Sandwich"]

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum

from api.models.ingredient import *


class Sandwich(models.Model):
    """샌드위치 모델"""

    name = models.CharField(
        "이름", unique=True, max_length=100, help_text="100자 이내. 중복 불가"
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

    bread = models.ManyToManyField(Bread, verbose_name="빵")
    topping = models.ManyToManyField(Topping, verbose_name="토핑")
    cheese = models.ManyToManyField(Cheese, verbose_name="치즈")
    sauce = models.ManyToManyField(Sauce, verbose_name="소스")

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
        return self.ingredients.aggregate(Sum("price"))["price__sum"]
