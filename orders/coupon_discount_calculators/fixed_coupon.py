from decimal import Decimal

from orders.models import Coupon, Order

from .coupon_discount_calculator import CouponDiscountCalculator


class FixedCoupon(CouponDiscountCalculator):
    def calculate(self, coupon: Coupon, order: Order) -> Decimal:
        if order.subtotal >= 1700:
            return coupon.discount_value
        else:
            return Decimal(0)
