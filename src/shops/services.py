from shops.models import Order, OrderItem, Product
from rest_framework.exceptions import ValidationError
from django.db import transaction
from django.db.models import Sum, F


class InventoryService:
    def check_and_update_stock(self, product: Product, quantity: int):
        if product.stock < quantity:
            raise ValidationError(f"{product.name}의 재고가 부족합니다.")
        product.stock -= quantity
        product.save()


class OrderService:
    def __init__(self, inventory_service):
        self.inventory_service = inventory_service

    @transaction.atomic
    def create_order(self, user, order_data):
        order = Order.objects.create(user=user)
        for item_data in order_data.get("items", []):
            product = Product.objects.get(id=item_data["product"])
            quantity = item_data["quantity"]
            self.inventory_service.check_and_update_stock(product, quantity)
            OrderItem.objects.create(order=order, product=product, quantity=quantity)
        self._calculate_total(order)
        return order

    def _calculate_total(order):
        total = order.items.aggregate(total_price=Sum(F("product__price") * F("quantity")))["total_price"] or 0
        order.total_price = total
        order.save()
        return total
