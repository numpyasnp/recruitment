from django.test import TestCase
from model_bakery import baker
from django.utils import timezone

from apps.hr_user.models import HRUser
from apps.hr_company.models import HRCompany
from apps.client_company.models import ClientCompany
from apps.job_posting.models import JobPosting
from apps.job_posting.tasks import DeactivateExpiredJobPostings


class DeactivateExpiredJobPostingsTaskTest(TestCase):
    def setUp(self):
        self.hr_company = baker.make(HRCompany)
        self.client_company = baker.make(ClientCompany)
        self.user = baker.make(HRUser, hr_company=self.hr_company, email="test@gmail.com", is_active=True)
        self.user.client_companies.add(self.client_company)

    def test_deactivate_expired_job_postings(self):
        yesterday = timezone.now().date() - timezone.timedelta(days=1)
        future = timezone.now().date() + timezone.timedelta(days=1)

        # Expired and active job posting (should be deactivated)
        expired_posting = baker.make(
            JobPosting,
            hr_user=self.user,
            hr_company=self.hr_company,
            client_company=self.client_company,
            closing_date=yesterday,
            is_active=True,
        )
        # Not expired, should remain active
        active_posting = baker.make(
            JobPosting,
            hr_user=self.user,
            hr_company=self.hr_company,
            client_company=self.client_company,
            closing_date=future,
            is_active=True,
        )
        self.assertEqual(JobPosting.objects.count(), 2)

        result = DeactivateExpiredJobPostings().run()
        expired_posting.refresh_from_db()
        active_posting.refresh_from_db()

        self.assertFalse(expired_posting.is_active)
        self.assertTrue(active_posting.is_active)
        self.assertIn("deactivated_count", result)
        self.assertEqual(result["deactivated_count"], 1)
        self.assertEqual(JobPosting.objects.active().count(), 1)
        self.assertEqual(JobPosting.objects.passive().count(), 1)
