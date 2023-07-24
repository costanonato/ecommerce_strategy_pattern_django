from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from orders.models import Coupon, Order
from orders.serializers import OrderSerializer


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
    coupon_code = request.data.get("coupon_code")
    coupon = get_object_or_404(Coupon, code=coupon_code)

    try:
        order.apply_discount_coupon(coupon)
        return Response(status=status.HTTP_204_NO_CONTENT)
    except ValueError as error:
        return Response({"error": str(error)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
