from typing import override
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import User


class JWTAuthTests(APITestCase):
    @override
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123", screen_name="Test"
        )

    def test_obtain_token(self):
        """Test getting JWT token"""
        data = {"username": "testuser", "password": "testpass123"}
        response = self.client.post("/api/v1/token/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_invalid_credentials(self):
        """Test token with wrong password"""
        data = {"username": "testuser", "password": "wrongpass"}
        response = self.client.post("/api/v1/token/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
