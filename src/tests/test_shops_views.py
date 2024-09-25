import pytest

pytestmark = pytest.mark.django_db


def test_create_order(client, sample_products):
    # Given
    items = [{"product": product.id, "quantity": 1} for product in sample_products]
    data = {"items": items}

    # When
    response = client.post("/api/orders/", data, format="json")

    # Then
    assert response.status_code == 201


def test_create_product_with_hstore_attributes(client):
    # Given
    data = {
        "name": "MacBook Pro M3",
        "price": 3300000,
        "stock": 10,
        "attributes": {"color": "Space Gray", "size": "13-inch"},
    }

    # When
    response = client.post("/api/products/", data, format="json")

    # Then
    assert response.status_code == 201
    assert response.data["attributes"] == {"color": "Space Gray", "size": "13-inch"}
