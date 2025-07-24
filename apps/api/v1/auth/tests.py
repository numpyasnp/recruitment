from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from model_bakery import baker

from apps.hr_user.models import HRUser
from libs.tests import create_hr_user
from django.utils.translation import gettext_lazy as _


class AuthSessionTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = "testpass123"
        cls.user = create_hr_user(password=cls.password)
        cls.user.set_password(cls.password)
        cls.user.save()

    def test_login_success(self):
        url = reverse("v1:auth:login")
        data = {"email": self.user.email, "password": self.password}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)

    def test_login_fail_wrong_password(self):
        url = reverse("v1:auth:login")
        data = {"email": self.user.email, "password": "wrongpass"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 404)
        self.assertIn(str(_("Account does not exists.")), str(response.data))

    def test_login_fail_wrong_email(self):
        url = reverse("v1:auth:login")
        data = {"email": "wrong@example.com", "password": self.password}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_logout_success(self):
        # Önce login ol
        self.client.login(email=self.user.email, password=self.password)
        url = reverse("v1:auth:logout")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)


class AuthJWTTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = "testpass123"
        cls.user = baker.make(HRUser, email="testuser@example.com", is_active=True)
        cls.user.set_password(cls.password)
        cls.user.save()

    def test_jwt_login_success(self):
        url = reverse("v1:auth:jwt_login")
        data = {"email": self.user.email, "password": self.password}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_jwt_login_fail_wrong_password(self):
        url = reverse("v1:auth:jwt_login")
        data = {"email": self.user.email, "password": "wrongpass"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_jwt_login_fail_wrong_email(self):
        url = reverse("v1:auth:jwt_login")
        data = {"email": "wrong@example.com", "password": self.password}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
