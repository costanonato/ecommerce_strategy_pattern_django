from abc import ABC, abstractmethod
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from orders.models import Coupon, Order


class CouponDiscountCalculator(ABC):
    @abstractmethod
    def calculate(self, coupon: "Coupon", order: "Order") -> Decimal:
        ...
