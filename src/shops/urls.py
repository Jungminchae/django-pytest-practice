from rest_framework.routers import DefaultRouter
from shops.views import OrderViewSet, ProductViewSet

router = DefaultRouter()
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"products", ProductViewSet, basename="product")

urlpatterns = router.urls
