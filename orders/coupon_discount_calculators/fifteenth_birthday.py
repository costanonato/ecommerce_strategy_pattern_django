from datetime import date
from decimal import Decimal

from orders.models import Coupon, Order

from .coupon_discount_calculator import CouponDiscountCalculator


class FifteenthBirthday(CouponDiscountCalculator):
    FIFTEENTH_BIRTHDAY_DATE = date(2023, 7, 24)

    def calculate(self, coupon: Coupon, order: Order) -> Decimal:
        if date.today() == self.FIFTEENTH_BIRTHDAY_DATE:
            return coupon.discount_value
        else:
            return Decimal(0)
