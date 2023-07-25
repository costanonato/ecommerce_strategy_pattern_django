from decimal import Decimal

from orders.models import Coupon, Order

from .coupon_discount_calculator import CouponDiscountCalculator


class PercentageCoupon(CouponDiscountCalculator):
    DISCOUNT_START_YEAR = 2023

    def calculate(self, coupon: Coupon, order: Order) -> Decimal:
        full_discount = (order.subtotal * coupon.discount_value) / 100

        if order.created_at.year >= self.DISCOUNT_START_YEAR:
            return full_discount
        else:
            return full_discount / 2
