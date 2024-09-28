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
    ("노트북", ["삼성 노트북 9", "LG 그램 14", "삼성 갤럭시북 이온"]),
    ("스마트폰", ["갤럭시 S21", "아이폰 12", "갤럭시 Z 플립", "갤럭시 노트 20"]),
    ("태블릿", ["아이패드 프로 11", "갤럭시 탭 S7", "아이패드 에어 4"]),
    ("모니터", ["LG 울트라파인 5K", "삼성 스마트 모니터 M7"]),
    ("스마트워치", ["애플워치 시리즈 6", "갤럭시 워치 3", "갤럭시 워치 액티브 2"]),
    ("데스크탑", ["삼성 데스크탑 5", "LG 일체형 PC", "애플 아이맥 27인치"]),
    ("이어폰", ["에어팟 프로", "갤럭시 버즈 프로", "에어팟 2세대"]),
    ("스피커", ["삼성 사운드바", "LG 엑스붐 AI 씽큐", "애플 홈팟"]),
]

# 임의의 가격과 재고 설정
base_price = Decimal("999.99")
base_stock = 100

# 가짜 데이터 생성
for product_category, models in products:
    for model in models:
        product_name = f"{product_category} {model}"
        attributes = {
            "brand": "삼성" if "삼성" in product_name else ("LG" if "LG" in product_name else "애플"),
            "category": product_category,
            "model": model,
        }

        baker.make(
            Product,
            name=product_name,
            description=f"{product_name}는 인기 있는 상품입니다!",
            price=base_price,
            stock=base_stock,
            attributes=attributes,
        )

print("한글 상품 데이터 생성이 완료되었습니다!")
