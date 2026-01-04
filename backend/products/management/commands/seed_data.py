from django.core.management.base import BaseCommand
from categories.models import Category
from products.models import Product

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # electronics, _ = Category.objects.get_or_create(name="Electronics")
        fashion, _ = Category.objects.get_or_create(name="Fashion")

        # Product.objects.get_or_create(
        #     name="iPhone 15",
        #     sku="IP15",
        #     description="Apple smartphone",
        #     price=1200,
        #     stock=10,
        #     category=electronics,
        #     status="active"
        # )

        Product.objects.get_or_create(
            name="T-Shirt",
            sku="TS01",
            description="Cotton T-Shirt",
            price=20,
            stock=50,
            category=fashion,
            status="active"
        )

        self.stdout.write(self.style.SUCCESS("Seed data created"))
