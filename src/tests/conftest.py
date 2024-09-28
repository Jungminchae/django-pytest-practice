import pytest
from itertools import cycle
from model_bakery import baker
from django.db import connection
from rest_framework.test import APIClient
from shops.services import InventoryService, OrderService


@pytest.fixture(scope="session")
def django_db_setup(django_db_blocker):
    """테스트 데이터베이스가 UP되었을 때 hstore 확장을 생성되어야 함"""
    with django_db_blocker.unblock():
        with connection.cursor() as cursor:
            cursor.execute("CREATE EXTENSION IF NOT EXISTS hstore;")
            cursor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")


@pytest.fixture
def sample_user(django_user_model):
    return django_user_model.objects.create_user(username="testuser", password="testpassword")


@pytest.fixture
def sample_products():
    prices = [1000, 2000, 3000]
    stocks = [10, 20, 30]
    return baker.make("shops.Product", _quantity=3, price=cycle(prices), stock=cycle(stocks))


@pytest.fixture
def sample_products2():
    products_name = ["MacBook Pro", "MacBook Air", "Dell XPS", "HP Spectre", "HP Envy"]
    prices = [2500, 1500, 2000, 1800]
    return baker.make("shops.Product", _quantity=4, name=cycle(products_name), price=cycle(prices))


@pytest.fixture
def hstore_products():
    attributes = [{"color": "Black", "size": "13-inch", "returned": True}, {"color": "White", "size": "15-inch", "weight": "1.5kg"}]
    return baker.make("shops.Product", _quantity=2, attributes=cycle(attributes))


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
