import pytest
from concurrent.futures import ThreadPoolExecutor
from shops.models import Product

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


def test_read_product_with_hstore_attributes(hstore_products):
    products = Product.objects.filter(attributes__has_key="weight")

    assert products.count() == 1
    assert products.first().attributes == {"color": "White", "size": "15-inch", "weight": "1.5kg"}


def test_read_product_with_hstore_attributes_has_any_key(hstore_products):
    products = Product.objects.filter(attributes__has_any_keys=["returned", "weight"])

    assert products.count() == 2
    assert products.first().attributes == {"color": "Black", "size": "13-inch", "returned": "True"}

@pytest.mark.django_db(transaction=True)
def test_product_update_with_concurrency_problem(db, client, sample_products):
    product = sample_products[0]
    product_id = product.id
    stock = product.stock -1

    def send_request(product_id, stock):
        return client.patch(f"/api/products/{product_id}/", {"stock": stock})
    
    with ThreadPoolExecutor() as executor:
        responses = executor.map(send_request, [product_id] * 5, [stock] * 5)
    
    status_codes = [response.status_code for response in responses]

    assert list(status_codes).count(200) == 1