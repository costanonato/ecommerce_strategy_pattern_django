from datetime import date
from decimal import Decimal

from django.db import models
from django.utils import timezone


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
        # [Aniversario15Anos]
        if self.code == "Aniversario15Anos":
            if date.today() == date(2023, 7, 24):
                return self.discount_value
            else:
                return Decimal(0)

        # [Percentage Discount]
        elif self.discount_type == self.DiscountTypes.PERCENTAGE:
            full_discount = (order.subtotal * self.discount_value) / 100

            if order.created_at.year >= 2023:
                return full_discount
            else:
                return full_discount / 2

        # [Fixed Discount]
        elif self.discount_type == self.DiscountTypes.FIXED:
            if order.subtotal >= 1700:
                return self.discount_value
            else:
                return Decimal(0)

        return Decimal(0)
