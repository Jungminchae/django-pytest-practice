import pytest
from itertools import cycle
from model_bakery import baker
from rest_framework.test import APIClient
from shops.services import InventoryService, OrderService


@pytest.fixture
def sample_user(django_user_model):
    return django_user_model.objects.create_user(username="testuser", password="testpassword")


@pytest.fixture
def sample_products():
    prices = [1000, 2000, 3000]
    stocks = [10, 20, 30]
    return baker.make("shops.Product", _quantity=3, price=cycle(prices), stock=cycle(stocks))


@pytest.fixture
def sample_order(sample_user, sample_products):
    order = baker.make("shops.Order", user=sample_user)
    for product in sample_products:
        baker.make("shops.OrderItem", order=order, product=product, quantity=1)
    return order


@pytest.fixture
def inventory_service():
    return InventoryService()


@pytest.fixture
def order_service(inventory_service):
    return OrderService(inventory_service)


@pytest.fixture
def client(sample_user):
    client = APIClient()
    client.force_login(sample_user)
    return client
