import pytest


pytestmark = pytest.mark.django_db


def test_create_order_with_sufficient_stock(order_service, sample_user, sample_products):
    # Given
    order_data = {"items": [{"product": sample_products[0].id, "quantity": 2}]}

    # When
    order = order_service.create_order(sample_user, order_data)

    # Then
    assert order.total_price == 2000
    assert order.items.count() == 1
    assert order.items.first().product.stock == 8
