from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from shops.filters import ProductFilterSet
from shops.models import Order, Product
from shops.serializers import OrderSerializer, ProductSerializer
from shops.services import OrderService
from shops.services import InventoryService


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request):
        user = request.user
        order_data = request.data
        inventory_service = InventoryService()
        order_service = OrderService(inventory_service)
        order = order_service.create_order(user, order_data)
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilterSet

    def update(self, request, *args, **kwargs):
        lock_id = f"product-update-lock-{self.kwargs['pk']}"
        lock = cache.lock(lock_id, timeout=3, blocking_timeout=1)

        try:
            acquired = lock.acquire(blocking=True)
            if acquired:
                response = super().update(request, *args, **kwargs)
                return response
            else:
                return Response({"error": "3초에 한 번만 수정할 수 있습니다."}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            