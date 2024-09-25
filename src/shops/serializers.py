from rest_framework import serializers
from shops.models import Product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price", "stock", "attributes"]

    def validate_attributes(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("Expected a dictionary of attributes.")

        for key, val in value.items():
            if not isinstance(val, str):
                value[key] = str(val)

        return value


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "user", "created_at", "total_price", "items"]
        read_only_fields = ["total_price", "created_at", "user"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order
