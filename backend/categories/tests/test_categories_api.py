from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from categories.models import Category

User = get_user_model()


class CategoryTest(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            email="admin@example.com", full_name="Admin User", password="admin123"
        )
        self.client.force_authenticate(user=self.admin)

    def test_create_category(self):
        response = self.client.post("/api/categories/", {"name": "Books"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Category.objects.count(), 1)

    def test_category_tree(self):
        parent = Category.objects.create(name="Electronics")
        Category.objects.create(name="Mobiles", parent=parent)

        response = self.client.get("/api/categories/categories/tree/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(len(response.data[0]["children"]), 1)

    def test_category_list(self):
        Category.objects.create(name="Fashion")
        Category.objects.create(name="Home Appliances")

        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def tearDown(self):
        self.client.logout()
