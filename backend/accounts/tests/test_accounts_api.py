from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AccountsAPITests(APITestCase):

    def setUp(self):
        self.register_url = "/api/accounts/register/"
        self.login_url = "/api/accounts/login/"
        self.profile_url = "/api/accounts/profile/"

        self.user_data = {
            "email": "testuser@example.com",
            "full_name": "Test User",
            "password": "securepassword123",
        }

    ## 1. Registration Tests
    def test_user_can_register(self):
        """Test if a user can register with valid data"""
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, self.user_data["email"])

    def test_registration_fails_without_email(self):
        """Test that email is mandatory for registration"""
        invalid_data = self.user_data.copy()
        invalid_data["email"] = ""
        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    ## 2. Login Tests
    def test_user_can_login(self):
        """Test if registered user receives JWT tokens on login"""
        # Create user first
        User.objects.create_user(**self.user_data)

        login_payload = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client.post(self.login_url, login_payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("is_admin", response.data)
        self.assertFalse(response.data["is_admin"])

    def test_login_with_invalid_credentials(self):
        """Test login fails with wrong password"""
        User.objects.create_user(**self.user_data)

        invalid_payload = {
            "email": self.user_data["email"],
            "password": "wrongpassword",
        }
        response = self.client.post(self.login_url, invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["non_field_errors"][0], "Invalid credentials")

    ## 3. Profile Tests
    def test_profile_access_denied_unauthenticated(self):
        """Test that profile view is protected"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_access_granted_authenticated(self):
        """Test profile view returns data for logged in user"""
        user = User.objects.create_user(**self.user_data)

        # Authenticate the test client
        self.client.force_authenticate(user=user)

        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], user.email)
        self.assertEqual(response.data["full_name"], user.full_name)

    ## 4. Admin Flag Test
    def test_login_returns_admin_status(self):
        """Verify is_admin is true for staff users"""
        admin_user = User.objects.create_superuser(
            email="admin@example.com", full_name="Admin User", password="adminpassword"
        )

        response = self.client.post(
            self.login_url, {"email": "admin@example.com", "password": "adminpassword"}
        )
        self.assertTrue(response.data["is_admin"])

    def test_login_returns_non_admin_status(self):
        """Verify is_admin is false for non-staff users"""
        normal_user = User.objects.create_user(**self.user_data)

        response = self.client.post(
            self.login_url,
            {"email": self.user_data["email"], "password": self.user_data["password"]},
        )
        self.assertFalse(response.data["is_admin"])

    def tearDown(self):
        self.client.logout()
