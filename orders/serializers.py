from rest_framework import serializers

from orders.models import Coupon, Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "subtotal", "total", "coupon_id", "created_at"]
