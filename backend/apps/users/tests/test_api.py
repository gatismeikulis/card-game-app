from typing import override
from rest_framework.test import APITestCase
from ..models import User


class UserListCreateRetrieveTests(APITestCase):
    """Tests for listing, retrieving and creating users (Public)"""

    @override
    @classmethod
    def setUpTestData(cls):
        cls.base_url: str = "/api/v1/users/"
        cls.sample_user1: User = User.objects.create_user(
            username="sampleuser1",
            email="sample1@example.com",
            password="samplepass123",
            screen_name="SampleUser1",
            description="First sample user",
        )

        cls.sample_user2: User = User.objects.create_user(
            username="sampleuser2",
            email="sample2@example.com",
            password="samplepass123",
            screen_name="SampleUser2",
            description="Second sample user",
        )

    def test_list_users_(self):
        """Test that user list returns correct data"""
        response = self.client.get(self.base_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        user_data = response.data[0]

        # Verify only public fields are present
        expected_fields = {"id", "screen_name"}
        self.assertEqual(set(user_data.keys()), expected_fields)

        # Verify expected values are correct
        self.assertEqual(response.data[0]["id"], self.sample_user1.pk)
        self.assertEqual(response.data[0]["screen_name"], self.sample_user1.screen_name)

    def test_get_user_detail(self):
        """Test that user detail returns correct data"""
        response = self.client.get(f"{self.base_url}{self.sample_user1.pk}/")
        self.assertEqual(response.status_code, 200)

        user_data = response.data

        # Verify only public fields are present
        expected_fields = {"id", "screen_name", "description", "date_joined"}
        self.assertEqual(set(user_data.keys()), expected_fields)

        # Verify expected values are correct
        self.assertEqual(response.data["id"], self.sample_user1.pk)
        self.assertEqual(response.data["screen_name"], self.sample_user1.screen_name)
        self.assertEqual(response.data["description"], self.sample_user1.description)

        # Verify sensitive fields are not exposed
        self.assertNotIn("email", response.data)
        self.assertNotIn("password", response.data)
        self.assertNotIn("username", response.data)

    def test_create_user(self):
        """Test that user can be created and listed"""
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "screen_name": "TestUser",
            "description": "Test user",
        }
        response1 = self.client.post(self.base_url, data)
        self.assertEqual(response1.status_code, 201)
        response2 = self.client.get(self.base_url)
        self.assertEqual(len(response2.data), 3)
