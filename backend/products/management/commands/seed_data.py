from django.core.management.base import BaseCommand

from categories.models import Category
from products.models import Product


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Parent categories
        electronics, _ = Category.objects.get_or_create(name="Electronics")
        fashion, _ = Category.objects.get_or_create(name="Fashion")
        computer, _ = Category.objects.get_or_create(name="Computer")
        # Child categories
        phone, _ = Category.objects.get_or_create(name="Phone", parent=electronics)

        # Products
        products = [
            {
                "name": "iPhone 15",
                "sku": "IP15",
                "description": "Apple smartphone",
                "price": 1200,
                "stock": 10,
                "category": phone,
                "status": "active",
            },
            {
                "name": "Samsung Galaxy S24",
                "sku": "SGS24",
                "description": "Samsung flagship smartphone",
                "price": 1100,
                "stock": 15,
                "category": phone,
                "status": "active",
            },
            {
                "name": "Google Pixel 8",
                "sku": "GP8",
                "description": "Google Pixel phone",
                "price": 900,
                "stock": 12,
                "category": phone,
                "status": "active",
            },
            {
                "name": "MacBook Air M2",
                "sku": "MBA-M2",
                "description": "Apple laptop with M2 chip",
                "price": 1500,
                "stock": 5,
                "category": computer,
                "status": "active",
            },
            {
                "name": "Dell XPS 13",
                "sku": "DX13",
                "description": "Premium ultrabook laptop",
                "price": 1400,
                "stock": 7,
                "category": computer,
                "status": "active",
            },
            {
                "name": "HP Pavilion 15",
                "sku": "HP15",
                "description": "Everyday laptop",
                "price": 900,
                "stock": 10,
                "category": computer,
                "status": "active",
            },
            {
                "name": "Men's T-Shirt",
                "sku": "TS01",
                "description": "Cotton T-Shirt",
                "price": 20,
                "stock": 50,
                "category": fashion,
                "status": "active",
            },
            {
                "name": "Women's Jeans",
                "sku": "WJ01",
                "description": "Denim jeans",
                "price": 45,
                "stock": 30,
                "category": fashion,
                "status": "active",
            },
            {
                "name": "Wireless Headphones",
                "sku": "WH01",
                "description": "Bluetooth headphones",
                "price": 150,
                "stock": 20,
                "category": electronics,
                "status": "active",
            },
            {
                "name": "Smart Watch",
                "sku": "SW01",
                "description": "Fitness smart watch",
                "price": 250,
                "stock": 18,
                "category": electronics,
                "status": "active",
            },
        ]

        for product in products:
            Product.objects.get_or_create(sku=product["sku"], defaults=product)

        self.stdout.write(
            self.style.SUCCESS("✅ Categories and 10 products seeded successfully")
        )
