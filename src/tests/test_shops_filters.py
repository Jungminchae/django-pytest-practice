import pytest
from shops.models import Product
from shops.filters import ProductFilterSet


@pytest.mark.django_db
def test_filter_by_name_similarity(sample_products2):
    queryset = Product.objects.all()
    filterset = ProductFilterSet(data={"search": "HP"}, queryset=queryset)
    filtered_qs = filterset.qs

    assert filtered_qs.count() == 2
    assert filtered_qs.first().name == "HP Spectre"
    assert filtered_qs.last().name == "HP Envy"
