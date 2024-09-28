import os
import sys
from pathlib import Path
from django import setup
from decimal import Decimal

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent / "src"

sys.path.append(str(PROJECT_ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pytest_example.settings")
setup()

from model_bakery import baker
from shops.models import Product

# 임의의 상품 카테고리와 모델명 설정
products = [
    ("MacBook", ["Pro 13-inch", "Pro 16-inch", "Air M1", "Air M2"]),
    ("Iphone", ["12", "12 Pro", "13", "13 Pro", "14", "14 Pro"]),
    ("IMac", ["21.5-inch", "27-inch", "24-inch"]),
    ("MacMini", ["M1", "M2", "Intel"]),
    ("AppleWatch", ["Series 6", "Series 7", "Series 8", "SE"]),
    ("GalaxyBook", ["Flex", "Ion", "Pro 360"]),
    ("GalaxyWatch", ["Active 2", "Watch 4", "Watch 5"]),
    ("GalaxyFold", ["Fold 2", "Fold 3", "Fold 4"]),
    ("Galaxy Z Flip", ["Flip 3", "Flip 4"]),
]

# 임의의 가격과 재고 설정
base_price = Decimal("999.99")
base_stock = 100

# 가짜 데이터 생성
for product_category, models in products:
    for model in models:
        product_name = f"{product_category} {model}"
        attributes = {
            "brand": "Apple" if "Galaxy" not in product_name else "Samsung",
            "category": product_category,
            "model": model,
        }

        baker.make(
            Product,
            name=product_name,
            description=f"{product_name} is a great product!",
            price=base_price,
            stock=base_stock,
            attributes=attributes,
        )

print("데이터 생성이 완료")
