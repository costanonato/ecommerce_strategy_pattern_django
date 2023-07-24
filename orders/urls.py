from django.urls import path

from . import views

urlpatterns = [
    path("<int:id>/", views.order_detail),
    path("<int:id>/apply_discount_coupon", views.apply_discount_coupon),
    path("", views.order_list),
]
