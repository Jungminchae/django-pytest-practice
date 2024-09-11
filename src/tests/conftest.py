import pytest
from itertools import cycle
from model_bakery import baker
from django.contrib.auth import get_user_model


@pytest.fixture
def sample_user():
    return get_user_model().objects.create_user(username="testuser", password="testpassword")


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
