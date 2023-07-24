from datetime import date
from decimal import Decimal

from django.db import models
from django.utils import timezone

from .coupon_discount_calculators.coupon_discount_calculator import (
    CouponDiscountCalculator,
)
from .coupon_discount_calculators.fifteenth_birthday import FifteenthBirthday
from .coupon_discount_calculators.fixed_coupon import FixedCoupon
from .coupon_discount_calculators.percentage_coupon import PercentageCoupon


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
    class DiscountTypes(models.IntegerChoices):
        PERCENTAGE = 1
        FIXED = 3

    discount_type = models.IntegerField(choices=DiscountTypes.choices)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    code = models.CharField(max_length=200)

    def calculate_discount_for(self, order: Order) -> Decimal:
        discount_calculator = self._get_discount_calculator()
        if discount_calculator is not None:
            return discount_calculator.calculate(self, order)
        else:
            return Decimal(0)

    def _get_discount_calculator(self) -> CouponDiscountCalculator | None:
        if self.code == "Aniversario15Anos":
            return FifteenthBirthday()
        elif self.discount_type == self.DiscountTypes.PERCENTAGE:
            return PercentageCoupon()
        elif self.discount_type == self.DiscountTypes.FIXED:
            return FixedCoupon()
