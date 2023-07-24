from abc import ABC, abstractmethod
from decimal import Decimal

from orders.models import Coupon, Order


class CouponDiscountCalculator(ABC):
    @abstractmethod
    def calculate(self, coupon: Coupon, order: Order) -> Decimal:
        pass
