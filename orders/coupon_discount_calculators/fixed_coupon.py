from decimal import Decimal

from orders.models import Coupon, Order

from .coupon_discount_calculator import CouponDiscountCalculator


class FixedCoupon(CouponDiscountCalculator):
    MINIMUM_SUBTOTAL_FOR_DISCOUNT = 1700

    def calculate(self, coupon: Coupon, order: Order) -> Decimal:
        if order.subtotal >= self.MINIMUM_SUBTOTAL_FOR_DISCOUNT:
            return coupon.discount_value
        else:
            return Decimal(0)
