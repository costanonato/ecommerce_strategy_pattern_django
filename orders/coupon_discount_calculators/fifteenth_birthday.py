from datetime import date
from decimal import Decimal

from orders.models import Coupon, Order

from .coupon_discount_calculator import CouponDiscountCalculator


class FifteenthBirthday(CouponDiscountCalculator):
    def calculate(self, coupon: Coupon, order: Order) -> Decimal:
        if date.today() == date(2023, 7, 24):
            return coupon.discount_value
        else:
            return Decimal(0)
