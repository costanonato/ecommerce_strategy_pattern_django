from decimal import Decimal
from typing import Any, Optional

from django.db import models
from django.utils import timezone

from .coupon_discount_calculators.coupon_discount_calculator import (
    CouponDiscountCalculator,
)


class Order(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    coupon = models.ForeignKey("Coupon", on_delete=models.CASCADE, null=True)

    def apply_discount_coupon(self, coupon: "Coupon"):
        discount = coupon.calculate_discount_for(self)
        if discount > 0:
            self.coupon = coupon
            self.total = max(self.subtotal - discount, 0)
            self.save()
        else:
            raise ValueError("Coupon not valid for this Order")


class Coupon(models.Model):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._discount_calculator = None

    class DiscountTypes(models.IntegerChoices):
        PERCENTAGE = 1
        FIXED = 3

    discount_type = models.IntegerField(choices=DiscountTypes.choices)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    code = models.CharField(max_length=200)

    def calculate_discount_for(self, order: Order) -> Decimal:
        if self._discount_calculator is not None:
            return self._discount_calculator.calculate(self, order)
        else:
            return Decimal(0)

    def set_discount_calculator(self, discount_calculator: Optional[CouponDiscountCalculator]):
        self._discount_calculator = discount_calculator
