from rest_framework.test import APITestCase
from rest_framework import status
from model_bakery import baker
from django.utils import timezone

from apps.hr_user.models import HRUser
from apps.hr_company.models import HRCompany
from apps.client_company.models import ClientCompany
from apps.job_posting.models import JobPosting


class JobPostingAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Test sınıfı başında 1 kere çalışır, tüm testlerde bu user kullanılır
        password = "testpass123"
        cls.hr_company = baker.make(HRCompany)
        cls.client_company = baker.make(ClientCompany)
        cls.user = baker.make(HRUser, hr_company=cls.hr_company, is_active=True, email="test@gmail.com")
        cls.user.set_password(password)
        cls.user.save()
        cls.user.client_companies.add(cls.client_company)

    def setUp(self):
        password = "testpass123"
        self.client.login(email=self.user.email, password=password)
        self.api_url = "/api/v1/job-postings/"

    def test_create_job_posting(self):
        data = {
            "hr_company": self.hr_company.id,
            "client_company": self.client_company.id,
            "title": "Test Job",
            "description": "Test description",
            "closing_date": timezone.now().date(),
            "is_active": True,
        }
        response = self.client.post(self.api_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(JobPosting.objects.count(), 1)
        self.assertEqual(JobPosting.objects.first().title, "Test Job")

    def test_list_job_postings(self):
        baker.make(
            JobPosting, hr_user=self.user, hr_company=self.hr_company, client_company=self.client_company, _quantity=3
        )
        response = self.client.get(self.api_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 3)

    def test_update_job_posting(self):
        job_posting = baker.make(
            JobPosting, hr_user=self.user, hr_company=self.hr_company, client_company=self.client_company
        )
        url = f"{self.api_url}{job_posting.id}/"
        data = {
            "title": "Updated Title",
            "hr_company": self.hr_company.id,
            "client_company": self.client_company.id,
            "hr_user": self.user.id,
            "closing_date": job_posting.closing_date,
            "is_active": job_posting.is_active,
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        job_posting.refresh_from_db()
        self.assertEqual(job_posting.title, "Updated Title")

    def test_delete_job_posting(self):
        job_posting = baker.make(
            JobPosting, hr_user=self.user, hr_company=self.hr_company, client_company=self.client_company
        )
        url = f"{self.api_url}{job_posting.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(JobPosting.objects.filter(id=job_posting.id).exists())

    def test_activate_job_posting(self):
        job_posting = baker.make(
            JobPosting,
            hr_user=self.user,
            hr_company=self.hr_company,
            client_company=self.client_company,
            is_active=False,
        )
        url = f"{self.api_url}{job_posting.id}/activate/"
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        job_posting.refresh_from_db()
        self.assertTrue(job_posting.is_active)

    def test_deactivate_job_posting(self):
        job_posting = baker.make(
            JobPosting,
            hr_user=self.user,
            hr_company=self.hr_company,
            client_company=self.client_company,
            is_active=True,
        )
        url = f"{self.api_url}{job_posting.id}/deactivate/"
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        job_posting.refresh_from_db()
        self.assertFalse(job_posting.is_active)
