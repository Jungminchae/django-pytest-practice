import pytest

pytestmark = pytest.mark.django_db


def test_create_order(client, sample_products):
    items = [{"product": product.id, "quantity": 1} for product in sample_products]
    data = {"items": items}
    response = client.post("/api/orders/", data, format="json")
    assert response.status_code == 201
