from django.db import models
from django.db.models import QuerySet
from django.utils import timezone

from apps.hr_user.models import HRUser
from libs.abstract.models import TimeStampedModel


class JobPostingQuerySet(QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def can_manage_job_post_by(self, user: HRUser):
        client_company_ids = user.client_companies.values_list("id", flat=True)
        return self.filter(hr_company=user.hr_company, client_company__id__in=[client_company_ids])

    def expired_active(self):
        today = timezone.now().date()
        return self.filter(is_active=True, closing_date__lt=today)


class JobPosting(TimeStampedModel):
    hr_user = models.ForeignKey("hr_user.HRUser", on_delete=models.DO_NOTHING, related_name="job_postings")
    hr_company = models.ForeignKey("hr_company.HRCompany", on_delete=models.CASCADE, related_name="job_postings")
    client_company = models.ForeignKey(
        "client_company.ClientCompany", on_delete=models.CASCADE, related_name="job_postings"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    closing_date = models.DateField()
    is_active = models.BooleanField(default=True)

    objects = JobPostingQuerySet.as_manager()

    class Meta:
        verbose_name = "Job Posting"
        verbose_name_plural = "Job Postings"
        db_table = "job_posting"

    def __str__(self):
        return f"{self.hr_user } - {self.title} ({self.client_company.name})"

    @property
    def is_hr_user_company_matched(self):
        return self.hr_company == self.hr_user.hr_company

    @property
    def is_hr_user_client_matched(self):
        return self.client_company in self.hr_user.client_companies.all()

    @property
    def is_manageable_by_hr_user(self):
        return self.is_hr_user_company_matched or self.is_hr_user_client_matched
