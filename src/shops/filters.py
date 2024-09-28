from django_filters.rest_framework import FilterSet
from django_filters import CharFilter
from django.contrib.postgres.search import TrigramSimilarity
from shops.models import Product


class ProductFilterSet(FilterSet):
    search = CharFilter(field_name="name", method="filter_by_name_similarity")
    search2 = CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Product
        fields = ("search", "search2")

    def filter_by_name_similarity(self, queryset, name, value):
        query = (
            queryset.annotate(
                similarity=TrigramSimilarity("name", value),
            )
            .filter(similarity__gte=0.2)
            .order_by("-similarity")
        )
        return query
