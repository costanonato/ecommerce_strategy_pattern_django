from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from orders.models import Coupon, Order
from orders.serializers import OrderSerializer

from .coupon_discount_calculators.fifteenth_birthday import FifteenthBirthday
from .coupon_discount_calculators.fixed_coupon import FixedCoupon
from .coupon_discount_calculators.percentage_coupon import PercentageCoupon


@api_view(["GET"])
def order_list(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def order_detail(request, id=None):
    order = Order.objects.get(pk=id)
    serializer = OrderSerializer(order)
    return Response(serializer.data)


@api_view(["PATCH"])
def apply_discount_coupon(request, id=None):
    order = Order.objects.get(pk=id)
    coupon = _load_coupon(request.data.get("coupon_code"))

    try:
        order.apply_discount_coupon(coupon)
        return Response(status=status.HTTP_204_NO_CONTENT)
    except ValueError as error:
        return Response({"error": str(error)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


def _load_coupon(coupon_code: str) -> Coupon:
    coupon = get_object_or_404(Coupon, code=coupon_code)
    discount_calculator = _get_discount_calculator_for(coupon)
    coupon.set_discount_calculator(discount_calculator)
    return coupon


def _get_discount_calculator_for(coupon: Coupon):
    if coupon.code == "Aniversario15Anos":
        return FifteenthBirthday()
    elif coupon.discount_type == coupon.DiscountTypes.PERCENTAGE:
        return PercentageCoupon()
    elif coupon.discount_type == coupon.DiscountTypes.FIXED:
        return FixedCoupon()
