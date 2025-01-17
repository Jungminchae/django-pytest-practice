# Generated by Django 5.1.1 on 2024-09-23 05:12

import pgtrigger.compiler
import pgtrigger.migrations
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0002_order_is_active_order_read_only_created_at_and_more'),
    ]

    operations = [
        pgtrigger.migrations.RemoveTrigger(
            model_name='orderitem',
            name='update_total_price_on_item_change',
        ),
        pgtrigger.migrations.AddTrigger(
            model_name='orderitem',
            trigger=pgtrigger.compiler.Trigger(name='update_total_price_on_item_change', sql=pgtrigger.compiler.UpsertTriggerSql(func='\n                    BEGIN\n                        UPDATE "order" \n                        SET total_price = (\n                            SELECT COALESCE(SUM(p.price * oi.quantity), 0)\n                            FROM order_item oi\n                            JOIN product p ON oi.product_id = p.id\n                            WHERE oi.order_id = NEW.order_id\n                        )\n                        WHERE id = NEW.order_id;\n\n                        RETURN NEW;\n                    END;\n                    ', hash='61ffa77e402ad688abe4e5895517deff3870cd3f', operation='INSERT OR DELETE OR UPDATE', pgid='pgtrigger_update_total_price_on_item_change_39ad0', table='order_item', when='BEFORE')),
        ),
    ]
