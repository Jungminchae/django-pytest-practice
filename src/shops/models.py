import pgtrigger
from django.db import models
from django.contrib.auth import get_user_model


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    class Meta:
        db_table = "product"

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "order"
        triggers = [
            pgtrigger.ReadOnly(
                name="read_only_created_at",
                fields=["created_at"],
            ),
            pgtrigger.SoftDelete(name="soft_delete", field="is_active"),
        ]

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        db_table = "order_item"
        triggers = [
            pgtrigger.Trigger(
                name="update_total_price_on_item_change",
                operation=pgtrigger.Insert | pgtrigger.Delete | pgtrigger.Update,
                when=pgtrigger.Before,
                func=pgtrigger.Func(
                    """
                    BEGIN
                        UPDATE "order" 
                        SET total_price = (
                            SELECT COALESCE(SUM(p.price * oi.quantity), 0)
                            FROM order_item oi
                            JOIN product p ON oi.product_id = p.id
                            WHERE oi.order_id = NEW.order_id
                        )
                        WHERE id = NEW.order_id;

                        RETURN NEW;
                    END;
                    """,
                ),
            ),
        ]

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
