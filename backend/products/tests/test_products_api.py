from categories.models import Category
from django.contrib.auth import get_user_model
from products.models import Product
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class ProductAPITest(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(
            email="admin@example.com", full_name="Admin User", password="admin123"
        )
        self.client.force_authenticate(user=self.admin)

        self.category = Category.objects.create(name="Electronics")

    def test_create_product(self):
        payload = {
            "name": "iPhone 15",
            "sku": "IP15",
            "description": "Latest iPhone",
            "price": 1200,
            "stock": 5,
            "status": "active",
            "category": self.category.id,
        }

        response = self.client.post("/api/products/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)

    def test_product_list(self):
        Product.objects.create(
            name="MacBook",
            sku="MBP",
            description="Laptop",
            price=2000,
            stock=3,
            status="active",
            category=self.category,
        )

        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_product_detail(self):
        product = Product.objects.create(
            name="iPad",
            sku="IPAD",
            description="Tablet",
            price=800,
            stock=10,
            status="active",
            category=self.category,
        )

        response = self.client.get(f"/api/products/{product.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "iPad")

    def test_update_product(self):
        product = Product.objects.create(
            name="AirPods",
            sku="APDS",
            description="Wireless Earbuds",
            price=200,
            stock=15,
            status="active",
            category=self.category,
        )

        payload = {
            "name": "AirPods Pro",
            "sku": "APDS",
            "description": "Wireless Earbuds with Noise Cancellation",
            "price": 250,
            "stock": 10,
            "status": "active",
            "category": self.category.id,
        }

        response = self.client.put(
            f"/api/products/{product.id}/", payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        self.assertEqual(product.name, "AirPods Pro")

    def test_delete_product(self):
        product = Product.objects.create(
            name="Apple Watch",
            sku="AWATCH",
            description="Smart Watch",
            price=400,
            stock=8,
            status="active",
            category=self.category,
        )

        response = self.client.delete(f"/api/products/{product.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def tearDown(self):
        self.client.logout()
